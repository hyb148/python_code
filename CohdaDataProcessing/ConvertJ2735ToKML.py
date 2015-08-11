#!/usr/bin/env python

"""
Process packet capture files and produce a KML of the BSMs.
"""

import os
import re
import sys
import array
import string
import WiresharkXML
import getopt
import binascii
import datetime
import xml.dom.minidom
import binascii
import struct
import copy

# By default we output the KML to stdout
OutFile = sys.stdout
# By default we don't produce terse (1Hz) output
Terse = False

class Element(xml.dom.minidom.Element):

    def writexml(self, writer, indent="", addindent="", newl=""):
        # indent = current indentation
        # addindent = indentation to add to higher levels
        # newl = newline string
        writer.write(indent+"<" + self.tagName)

        attrs = self._get_attributes()
        a_names = attrs.keys()
        a_names.sort()

        for a_name in a_names:
            writer.write(" %s=\"" % a_name)
            xml.dom.minidom._write_data(writer, attrs[a_name].value)
            writer.write("\"")
        if self.childNodes:
            newl2 = newl
            if len(self.childNodes) == 1 and \
                self.childNodes[0].nodeType == xml.dom.minidom.Node.TEXT_NODE:
                indent, addindent, newl = "", "", ""
            writer.write(">%s"%(newl))
            for node in self.childNodes:
                node.writexml(writer,indent+addindent,addindent,newl)
            writer.write("%s</%s>%s" % (indent,self.tagName,newl2))
        else:
            writer.write("/>%s"%(newl))

# Monkey patch Element class to use our subclass instead.
xml.dom.minidom.Element = Element

class KML:
  """."""

  def __init__ (self, Title, Description=''):
    """."""
    self.KML = self.CreateDocument(Title, Description)
    self.Doc = self.KML.documentElement.getElementsByTagName('Document')[0]

    self.Colors = [ \
        "FF000000", "FF00FF00", "FF0000FF", "FFFFFF00", "FFFF00FF", "FF00FFFF", "FF000000", \
        "80000000", "FF008000", "FF000080", "FF808000", "FF800080", "FF008080", "FF808080", \
        "C0000000", "FF00C000", "FF0000C0", "FFC0C000", "FFC000C0", "FF00C0C0", "FFC0C0C0", \
        "40000000", "FF004000", "FF000040", "FF404000", "FF400040", "FF004040", "FF404040", \
        "20000000", "FF002000", "FF000020", "FF202000", "FF200020", "FF002020", "FF202020", \
        "60000000", "FF006000", "FF000060", "FF606000", "FF600060", "FF006060", "FF606060", \
        "A0000000", "FF00A000", "FF0000A0", "FFA0A000", "FFA000A0", "FF00A0A0", "FFA0A0A0", \
        "E0000000", "FF00E000", "FF0000E0", "FFE0E000", "FFE000E0", "FF00E0E0", "FFE0E0E0", \
    ]
    self.ColorIdx = 0;

  def CreateDocument (self, Title, Description=None):
    """Create the overall KML document."""
    Doc = xml.dom.minidom.Document()
    KML = Doc.createElement('kml')
    KML.setAttribute('xmlns', 'http://www.opengis.net/kml/2.2')
    Doc.appendChild(KML)
    Document = Doc.createElement('Document')
    KML.appendChild(Document)
    DocName = Doc.createElement('name')
    Document.appendChild(DocName)
    DocNameText = Doc.createTextNode(Title)
    DocName.appendChild(DocNameText)
    if Description:
      DocDesc = Doc.createElement('description')
      Document.appendChild(DocDesc)
      DocDescText = Doc.createTextNode(Description)
      DocDesc.appendChild(DocDescText)
    return Doc


  def CreateStyle (self, Id, URL):
    """
    Create a new style for different placemark icons:

    <Style id=$Id>
      <IconStyle>
        <color>ffffffff</color>
        <scale>0.5</scale>
        <Icon>
          <href>$URL</href>
        </Icon>
      </IconStyle>
      <LineStyle>
        <color>ffffffff</color>
        <width>0.5</width>
      </LineStyle>
    </Style>
    """

    self.ColorIdx += 1
    self.ColorIdx %= len(self.Colors)
    Doc = xml.dom.minidom.Document()
    # <Style>
    Style = Doc.createElement('Style')
    Style.setAttribute('id', Id)
    Doc.appendChild(Style)
    # <IconStyle>
    IconStyle = Doc.createElement('IconStyle')
    Style.appendChild(IconStyle)
    # <color>
    IconColor = Doc.createElement('color')
    IconColorText = Doc.createTextNode(self.Colors[self.ColorIdx])
    IconColor.appendChild(IconColorText)
    IconStyle.appendChild(IconColor)
    # <Scale>
    IconScale = Doc.createElement('scale')
    IconScaleText = Doc.createTextNode('0.5')
    IconScale.appendChild(IconScaleText)
    IconStyle.appendChild(IconScale)
    # <Icon>
    Icon = Doc.createElement('Icon')
    IconStyle.appendChild(Icon)
    HRef = Doc.createElement('href')
    Icon.appendChild(HRef)
    HRefText = Doc.createTextNode(URL)
    HRef.appendChild(HRefText)
    # <LineStyle>
    LineStyle = Doc.createElement('LineStyle')
    Style.appendChild(LineStyle)
    # <color>
    LineColor = Doc.createElement('color')
    LineColorText = Doc.createTextNode(self.Colors[self.ColorIdx])
    LineColor.appendChild(LineColorText)
    LineStyle.appendChild(LineColor)
    # <Scale>
    LineScale = Doc.createElement('scale')
    LineScaleText = Doc.createTextNode('0.5')
    LineScale.appendChild(LineScaleText)
    LineStyle.appendChild(LineScale)
    return Doc

  def AddStyle(self, Id='None', \
               URL='http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'):
    """."""
    Style = self.CreateStyle(Id, URL)
    self.Doc.appendChild(Style.documentElement)

  def CreatePos(self, Id='None', Details={}):
    """
    Generate the KML Placemark for a given address.
      <Placemark>
        <description>
        RxTime:  $Details['Time']
        SecMark: $Details['SecMark']
        TmpId:   $Details['TmpId']
        PSID:    $Details['PSID']
        Speed:   $Details['Speed']
        Events:  $Details['Events']
        </description>
        <styleUrl>#$Id</styleUrl>
        <TimeStamp><when>2012-01-31T18:43:30.845Z</when></TimeStamp>
        <Point><coordinates>-83.538634,40.304202,0.000000</coordinates></Point>
      </Placemark>
    """
    Doc = xml.dom.minidom.Document()
    Placemark = Doc.createElement("Placemark")
    Doc.appendChild(Placemark)
    Desc = Doc.createElement("description")
    Placemark.appendChild(Desc)
    Txt = ''
    Txt += 'Received: %(Time)s\n'    % (Details)
    Txt += 'SecMark:  %(SecMark)s\n' % (Details)
    Txt += 'TmpId:    %(TmpId)s\n'   % (Details)
    Txt += 'PSID:     %(PSID)s\n'    % (Details)
    Txt += 'Speed:    %(Speed)s\n'    % (Details)
    Txt += 'Events:   %(Events)s\n'    % (Details)
    DescText = Doc.createTextNode(Txt)
    Desc.appendChild(DescText)
    Style = Doc.createElement("styleUrl")
    Placemark.appendChild(Style)
    StyleText = Doc.createTextNode('#%s' % (Id))
    Style.appendChild(StyleText)
    Timestamp = Doc.createElement("TimeStamp")
    Placemark.appendChild(Timestamp)
    When = Doc.createElement("when")
    Timestamp.appendChild(When)
    WhenText = Doc.createTextNode('%(Date)sT%(Time)sZ' % Details)
    When.appendChild(WhenText)
    Point = Doc.createElement("Point")
    Placemark.appendChild(Point)
    Coords = Doc.createElement("coordinates")
    Point.appendChild(Coords)
    CoordsText = Doc.createTextNode('%(Lon)f,%(Lat)f,%(Elev)f' % Details)
    Coords.appendChild(CoordsText)
    return Doc

  def CreateLine(self, Id='None', Details={}):
    """
    Generate the KML Placemark for a given address.
      <Placemark>
        <styleUrl>#$Id</styleUrl>
        <TimeStamp><when>2012-01-31T18:43:30.845Z</when></TimeStamp>
        <LineString><coordinates>...</coordinates></LineString>
      </Placemark>
    """
    Doc = xml.dom.minidom.Document()
    Placemark = Doc.createElement("Placemark")
    Doc.appendChild(Placemark)
    Style = Doc.createElement("styleUrl")
    Placemark.appendChild(Style)
    StyleText = Doc.createTextNode('#%s' % (Id))
    Style.appendChild(StyleText)
    Timestamp = Doc.createElement("TimeStamp")
    Placemark.appendChild(Timestamp)
    When = Doc.createElement("when")
    Timestamp.appendChild(When)
    WhenText = Doc.createTextNode('%(Date)sT%(Time)sZ' % Details)
    When.appendChild(WhenText)
    LineString = Doc.createElement("LineString")
    Placemark.appendChild(LineString)
    Crumbs = Doc.createElement("coordinates")
    LineString.appendChild(Crumbs)
    Txt = '%(Lon)f,%(Lat)f,%(Elev)f ' % Details
    for Crumb in Details['PathHistory']:
      Lat = Details['Lat'] - Crumb['LatOffset']
      Lon = Details['Lon'] - Crumb['LonOffset']
      Alt = Details['Elev'] - Crumb['ElevOffset']
      Txt += '%f,%f,%f ' % (Lon, Lat, Alt)
    CrumbsText = Doc.createTextNode(Txt)
    Crumbs.appendChild(CrumbsText)
    return Doc

  def AddPlacemark(self, Id='None', Details=None):
    """."""
    Placemark = self.CreatePos(Id, Details)
    self.Doc.appendChild(Placemark.documentElement)
    Placemark = self.CreateLine(Id, Details)
    self.Doc.appendChild(Placemark.documentElement)

  def Print (self):
    print self.KML.toprettyxml(indent="  ", encoding='UTF-8')


class Entity:
  """
  Keeps track of a single MAC+TmpId's messages
  """
  def __init__ (self):
    self.Msgs = []

  def Add (self, Detail):
    self.Msgs.append(Detail)

  def CSV (self):
    print 'date, time, lat, lon'
    for Msg in self.Msgs:
      print '%s, %s, %.7f, %.7f' % (Msg['Date'], Msg['Time'], Msg['Lat'], Msg['Lon'])


class CaptureFile:
  """
  Parses a single a capture file and keeps track of all MACs in the file.
  """

  def __init__ (self, Filename):
    """
    Run tshark on the capture file and parse the data.
    """
    self.Entities = {}
    Name = os.path.basename(Filename)
    Desc = None
    self.Out = KML(Name, Desc)

    Pipe = os.popen("tshark -Tpdml -n -Y '!(_ws.malformed) && (j2735.msgID == 2)' -r " + Filename, "r")
    WiresharkXML.parse_fh(Pipe, self.Collect)

  def Collect (self, Packet):
    """
    Collect the packets passed back from WiresharkXML.
    """
    Epoch   = Packet.get_items("frame.time_epoch" )[-1].get_show()
    try:
      Src   = Packet.get_items('eth.src')[-1].get_show()
    except:
      pass
    try:
      Src   = Packet.get_items('wlan.sa')[-1].get_show()
    except:
      pass
    try:
      Src   = Packet.get_items('cohda.wsm.SA')[-1].get_show()
    except:
      pass
    try:
      Src   = Packet.get_items('cohda.wsm.DA')[-1].get_show()
    except:
      pass
    TmpId   = Packet.get_items("j2735.id")[0].get_value()
    SecMark = Packet.get_items("j2735.secMark")[0].get_value()
    Lat     = Packet.get_items("j2735.lat")[0].get_value()
    Lon     = Packet.get_items("j2735.long")[0].get_value()
    Speed   = Packet.get_items("j2735.blob.speed")[0].get_value()
    Elev    = Packet.get_items("j2735.blob.elev")[0].get_value()
    Heading = Packet.get_items("j2735.heading")[0].get_value()
    try:
      PSID  = Packet.get_items("16093.psid")[0].get_value()
    except:
      pass
    try:
      PSID  = Packet.get_items("cohda.wsm.psid")[0].get_value()
    except:
      pass
    try:
      PH    = Packet.get_items("j2735.pathHistoryPointSets_04")[0].get_value()
    except:
      PH = ''
    try:
      Events = Packet.get_items("j2735.events")[0].get_value()
    except:
      Events = 0


    def Int64 (h):
      return int(h, 16) if int(h,16) < int('0x8000000000000000', 16) else (-int('0xffffffffffffffff', 16)+int(h,16)-1)
    def Int32 (h):
      return int(h, 16) if int(h,16) < int('0x80000000', 16) else (-int('0xffffffff', 16)+int(h,16)-1)
    def Int16 (h):
      return int(h, 16) if int(h,16) < int('0x8000', 16) else (-int('0xffff', 16)+int(h,16)-1)
    def Int8 (h):
      return int(h, 16) if int(h,16) < int('0x80', 16) else (-int('0xff', 16)+int(h,16)-1)

    Lat     = Int32(Lat) / 1e7
    Lon     = Int32(Lon) / 1e7
    Epoch = float(Epoch)
    DateTime = datetime.datetime.utcfromtimestamp(Epoch)
    Date = DateTime.strftime('%Y-%m-%d')
    Time = DateTime.strftime("%H:%M:%S.%f")
    SecMark = int(SecMark, 16)
    Speed   = (int(Elev, 16) & 0x1FFF) / 100.0
    try:
      Elev    = Int16(Elev, 16) * 0.1
    except:
      Elev    = 0.0
    Heading = int(Heading, 16) * 0.0125

    # PathHistoryPointType-04 ::= OCTET STRING (SIZE(8))
    # latOffset  INTEGER (-131072..131071) (18 signed bits)
    # longOffset INTEGER (-131072..131071) (18 signed bits)
    #  in 1/10th micro degrees
    #  value  131071 to be used for  131071 or greater
    #  value -131071 to be used for -131071 or less
    #  value -131072 to be used for unavailable lat or long
    # elevationOffset    INTEGER (-2048..2047), (12 signed bits)
    #  LSB units of 10 cm
    #  value  2047 to be used for  2047 or greater
    #  value -2047 to be used for -2047 or greater
    #  value -2048 to be unavailable
    # timeOffset INTEGER (0..65535), (16 unsigned bits)
    #  LSB units of of 10 mSec
    #  value  65534 to be used for 65534 or greater
    #  value  65535 to be unavailable
    PH4 = []
    for i in range(0, len(PH), 16):
      Bytes = binascii.unhexlify(PH[i:i + 16])
      if len(Bytes) != 8: continue
      ( Val, ) = struct.unpack('!Q', Bytes)
      if Val == 0: continue
      # from LSB to MSB
      # 16 bits timeOffset
      TimeOffset = Val & 0xffff
      TimeOffset = TimeOffset * 0.01
      Val = Val >> 16
      # 12 bits eleOffset
      # TODO: units
      ElevOffset = Val & 0xfff
      if (ElevOffset >= 0x800): ElevOffset = -int('0xfff', 16) + ElevOffset -1
      ElevOffset = ElevOffset * 0.1
      Val = Val >> 12
      # 18 bits lonOffset
      LonOffset = Val & 0x3ffff
      if (LonOffset >= 0x20000): LonOffset = -int('0x3ffff', 16) + LonOffset -1
      LonOffset = LonOffset * 0.0000001
      Val = Val >> 18
      # 18 bits latOffset
      LatOffset = Val & 0x3ffff
      if (LatOffset >= 0x20000): LatOffset = -int('0x3ffff', 16) + LatOffset -1
      LatOffset = LatOffset * 0.0000001
      Crumb = { 'LatOffset': LatOffset, 'LonOffset': LonOffset,
                'ElevOffset': ElevOffset, 'TimeOffset': TimeOffset }
      PH4.append(Crumb)

    Details = { 'Epoch':   Epoch,
                'Date':    Date,
                'Time':    Time,
                'Src':     Src,
                'PSID':    PSID,
                'TmpId':   TmpId,
                'SecMark': SecMark,
                'Lat':     Lat,
                'Lon':     Lon,
                'Elev':    Elev,
                'Speed':   Speed,
                'Heading': Heading,
                'PathHistory': PH4,
                'Events': Events }

    # In 'terse' mode: Only process elements withing 50ms of the second boudary
    global Terse
    if Terse == True:
      Remainder = Epoch % 1.000
      if (Remainder > 0.050) and (Remainder < 0.950):
        return

    Key = TmpId
    if not self.Entities.has_key(Key):
      Ent = self.Entities[Key] = Entity()
      self.Out.AddStyle(Key)
    else:
      Ent = self.Entities[Key]
    Ent.Add(Details)
    self.Out.AddPlacemark(Key, Details)

  def Print(self):
    if not self.Entities:
      return
    self.Out.Print()

def ProcessFilename (Filename):
  """Process one capture file."""
  Capture = CaptureFile(Filename)
  Capture.Print()

def Process (Filenames):
  """."""
  for Filename in Filenames:
    Cmd = 'mergecap -w %s. %s' % (Filename, Filename)
    os.system(Cmd)
    ProcessFilename(Filename + '.')
    os.unlink(Filename + '.')

def Usage():
  print >> sys.stderr, "ConvertJ2735ToKML.py [OPTIONS] CAPTURE_FILE [...]"
  print >> sys.stderr, "  -o FILE       name of output file"
  print >> sys.stderr, "  -t            Produce terse (1Hz) output"
  sys.exit(1)

def Main(Argv=sys.argv):

  optstring = "ho:t"
  longopts = ["help"]

  try:
    opts, args = getopt.getopt(Argv[1:], optstring, longopts)
  except getopt.GetoptError:
    usage()

  for opt, arg in opts:
    if opt == "-h" or opt == "--help":
      Usage()

    elif opt == "-o":
      Filename = arg
      global OutFile
      try:
        OutFile = open(Filename, "w")
      except IOError:
        sys.exit("Could not open %s for writing." % (Filename,))

    elif opt == "-t":
      global Terse
      Terse = True

    else:
      sys.exit("Unhandled command-line option: " + opt)
  Process(args)

#------------------------------------------------------------------------------
# Main Program
#------------------------------------------------------------------------------
if __name__ == '__main__':
  Main(sys.argv)

