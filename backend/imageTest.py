import model.preprocess as pp

filepath = "putwriting.png"

linebounds = pp.textDetect(filepath)

pp.charSegment(filepath, linebounds)