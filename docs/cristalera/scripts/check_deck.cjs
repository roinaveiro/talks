/* Browser audit and PDF export.
 * PLAYWRIGHT_MODULE may point to an installed playwright or playwright-core package.
 */
const fs = require('fs');
const path = require('path');
const {pathToFileURL} = require('url');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');

(async () => {
  const reviewDir = process.env.DECK_REVIEW_DIR || '/tmp/cristalera-review';
  fs.mkdirSync(reviewDir, {recursive: true});
  const browser = await chromium.launch({headless: true, args: ['--no-sandbox']});
  const report = {};
  for (const name of ['secure-ml', 'secure-ml-appendix']) {
    const page = await browser.newPage({viewport: {width: 1280, height: 720}, deviceScaleFactor: 1});
    const errors = [];
    const blockedRequests = [];
    await page.route(/^https?:\/\//, route => {
      blockedRequests.push(route.request().url());
      return route.abort();
    });
    page.on('pageerror', e => errors.push(String(e)));
    const uri = pathToFileURL(path.resolve(name + '.html')).href;
    await page.goto(uri, {waitUntil: 'networkidle'});
    await page.waitForFunction(() => typeof Reveal !== 'undefined' && Reveal.isReady());
    // Freeze fragment fades so screenshots capture the fully visible state.
    await page.addStyleTag({content: '.reveal .fragment { transition: none !important; }'});
    await page.evaluate(() => {
      Reveal.configure({transition: 'none'});
      document.querySelectorAll('.fragment').forEach(e => e.classList.add('visible'));
    });
    await page.waitForTimeout(200);
    const slides = await page.evaluate(() => Reveal.getSlides().map(s => ({id: s.id, title: s.querySelector('h2')?.textContent})));
    const entries = [];
    for (let i=0; i<slides.length; i++) {
      await page.evaluate(i => {
        Reveal.slide(i, 0);
        document.querySelectorAll('.fragment').forEach(e => e.classList.add('visible'));
      }, i);
      await page.waitForTimeout(40);
      const entry = await page.evaluate(() => {
        const s = Reveal.getCurrentSlide();
        const hidden = e => e.closest('aside.notes, .speaker-notes, .source, .section-kicker') ||
          getComputedStyle(e).display === 'none' || getComputedStyle(e).visibility === 'hidden';
        const clippedByAncestor = e => {
          for(let a=e.parentElement; a && a!==s; a=a.parentElement)
            if(['hidden','clip'].includes(getComputedStyle(a).overflow)) return true;
          return false;
        };
        const r = s.getBoundingClientRect();
        const overflow = [...s.querySelectorAll('h2,p,li,table,.katex-display,img,blockquote,.takeaway,.prompt')]
          .filter(e => !hidden(e) && !clippedByAncestor(e))
          .map(e => {
            const b=e.getBoundingClientRect();
            return {tag:e.tagName, text:(e.innerText||e.alt||'').slice(0,110),
              x:b.x,y:b.y,right:b.right,bottom:b.bottom,width:b.width,height:b.height};
          }).filter(b => b.width>0 && b.height>0 &&
            (b.x < r.x-3 || b.right > r.right+3 || b.y < r.y-3 || b.bottom > r.bottom-32));
        return {id:s.id, overflow, notes: !!s.querySelector('aside.notes')};
      });
      entries.push(entry);
      if (name==='secure-ml' || process.env.AUDIT_APPENDIX_IMAGES==='1')
        await page.screenshot({path:path.join(reviewDir, name+'-'+String(i+1).padStart(2,'0')+'.png')});
    }
    const state = await page.evaluate(() => ({
      mathErrors:[...document.querySelectorAll('.katex-error')].map(e=>e.textContent),
      brokenImages:[...document.images].filter(e=>!e.complete||e.naturalWidth===0).map(e=>e.alt),
      mathCount: document.querySelectorAll('.katex').length,
      externalScripts:[...document.scripts].map(s=>s.src).filter(s=>/^https?:/.test(s)),
      sourceCount: document.querySelectorAll('section.slide .source').length
    }));
    report[name] = {slideCount: slides.length, slides: entries, pageErrors: errors, blockedRequests, ...state};
    await page.close();
    if (process.env.DECK_EXPORT_PDF !== '0') {
      const print = await browser.newPage({viewport:{width:1280,height:720}});
      await print.route(/^https?:\/\//, route => route.abort());
      await print.goto(uri+'?print-pdf', {waitUntil:'networkidle'});
      await print.waitForFunction(() => document.querySelectorAll('.pdf-page').length > 0);
      await print.emulateMedia({media:'print'});
      await print.waitForTimeout(500);
      report[name].printOverflow = await print.evaluate(() =>
        [...document.querySelectorAll('.pdf-page section.slide')].flatMap(s => {
          const r=s.getBoundingClientRect();
          return [...s.querySelectorAll('h2,p,li,table,.katex-display,img')]
            .filter(e => !e.closest('aside.notes,.source,.section-kicker') &&
              getComputedStyle(e).display!=='none' && getComputedStyle(e).visibility!=='hidden')
            .filter(e => {
              for(let a=e.parentElement;a && a!==s;a=a.parentElement)
                if(['hidden','clip'].includes(getComputedStyle(a).overflow))return false;
              const b=e.getBoundingClientRect();
              return b.width>0 && b.height>0 && (b.left<r.left-3||b.right>r.right+3||b.bottom>r.bottom-32);
            }).map(e=>({id:s.id,text:(e.innerText||e.alt||'').slice(0,90)}));
        }));
      await print.pdf({path:path.resolve(name+'.pdf'),printBackground:true,
        preferCSSPageSize:true,margin:{top:0,bottom:0,left:0,right:0}});
      report[name].pdfPages = await print.locator('.pdf-page').count();
      await print.close();
    }
    console.log(name,JSON.stringify({
      slides:report[name].slideCount,overflowSlides:entries.filter(e=>e.overflow.length).map(e=>e.id),
      missingNotes:entries.filter(e=>!e.notes).map(e=>e.id),...state,pageErrors:errors,blockedRequests,
      printOverflow:report[name].printOverflow
    }));
  }
  fs.writeFileSync(path.join(reviewDir,'layout-report.json'),JSON.stringify(report,null,2));
  await browser.close();
  if (Object.values(report).some(r => r.pageErrors.length || r.mathErrors.length ||
      r.brokenImages.length || r.blockedRequests.length || r.externalScripts.length ||
      r.slides.some(s => s.overflow.length || !s.notes) || (r.printOverflow || []).length))
    process.exitCode = 1;
})().catch(e => { console.error(e); process.exitCode=1; });
