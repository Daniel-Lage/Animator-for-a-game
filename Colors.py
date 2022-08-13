def Color(color="000000"):  # function disguised as a class
    red = (int(color[0], 16) * 16) + int(color[1], 16)
    green = (int(color[2], 16) * 16) + int(color[3], 16)
    blue = (int(color[4], 16) * 16) + int(color[5], 16)
    return red, green, blue


Text = Color("000000")
UIBackground = Color("FFFFFF")
UIBackgroundHovered = Color("CCCCCC")
Background = Color("303030")
# Borders = Color("66666A")
Selection = Color("3F647F")
SelectionBorder = Color("7FC9FF")
