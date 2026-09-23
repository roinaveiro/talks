-- Draft manuscripts stay local. Preserve their citation text in the public
-- presentation without creating links to unpublished source folders.
function Link(link)
  if link.target:match('^context/') then
    return pandoc.Span(link.content)
  end
  return link
end
