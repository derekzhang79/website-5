$ ->
  init()

expanda = (item) ->
  console.log 'pew'


init = (x) ->
  console.log 'ineeeet'

  $('#rombs .romb').each (i, element)  =>

    $(element).click ->

      $(element).css({'z-index': -1, 'background-color': '#666'})

      $(element).animate({
        rotate: '0deg',
        width: '60px',
        height: '60px',
        marginLeft: '+=2px',
        marginTop: '+=2px'
      }, 500)


    $(element).animate({rotate: '45deg'}, 1 );