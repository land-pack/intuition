def image_resize(im, pixellimit):

  width, height = im.size

  if width > height:
    #Land scape mode. Scale to width.

    aspectRatio = float(height)/float(width)
    Scaledwidth = pixellimit
    Scaledheight = int(round(Scaledwidth * aspectRatio))
    newSize = (Scaledwidth, Scaledheight)
  elif height > width:
    #Portrait mode, Scale to height.
    aspectRatio = float(width)/float(height)
    Scaledheight = pixellimit
    Scaledwidth = int(round(Scaledheight * aspectRatio))
    newSize = (Scaledwidth, Scaledheight)

  #FAILS RIGHT HERE... I double checked by writing print flags all over, and it so happens nothing past this line gets written
  imageThumbnail = im.resize(newSize)

  return imageThumbnail
