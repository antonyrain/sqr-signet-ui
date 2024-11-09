import rhinoscriptsyntax as rs
from Rhino.UI import *
from Eto.Forms import *
from Eto.Drawing import *

class BuildArgs():
    
    # Initializer
    def __init__(self):
        self.RingSize_ = 20
        self.SqrSide_ = 10
        self.TopArcFactor_ = 1
        self.Border_ = 1
        self.Depth_ = 2
        self.TopThickness_ = 3
        self.SideArcFactor_ = 0.7
        self.BottomAndSideThickness_ = 1
        self.BottomArcFactor_ = 0.5
        self.BottomWidth_ = 3

        self.CutWindow_ = False
        self.FullyFilled_ = True
        self.MovePrevious_ = False
        self.AxisButtonlist_ = None

    # Validator
    def IsValid(self):
        # You can do some general validations here
        return True

class BuildDialog(Dialog[bool]):
    
    def __init__(self, args):
        self.Args = args
        self.Title = 'Sqr Top Ring'
        self.Padding = Padding(10)
        # Create layout
        layout = TableLayout()
        layout.Padding = Padding(10)
        layout.Spacing = Size(10, 10)
        layout.Rows.Add(self.CreateSteppers())
        layout.Rows.Add(self.CreateCheckBoxes())
        layout.Rows.Add(None) # spacer
        layout.Rows.Add(self.CreateButtons())
        layout.Rows.Add(None) # spacer
        # Set the dialog content
        self.Content = layout
    
    # Creates numeric controls
    def CreateSteppers(self):
        # Create labels
        label0 = Label(Text = 'Ring size:')
        label1 = Label(Text = 'Square side:')
        label2 = Label(Text = 'Top arc factor:')
        label3 = Label(Text = 'Border:')
        label4 = Label(Text = 'Depth:')
        label5 = Label(Text = 'Top thickness:')
        label6 = Label(Text = 'Side arc factor:')
        label7 = Label(Text = 'Bottom thickness:')
        label8 = Label(Text = 'Bottom arc factor:')
        label9 = Label(Text = 'Bottom width:')

        self.RingSize_ = NumericUpDown()
        self.RingSize_.DecimalPlaces = 2
        self.RingSize_.Increment = 0.01
        self.RingSize_.MaxValue = 30.0
        self.RingSize_.MinValue = 10
        self.RingSize_.Value = 20

        self.SqrSide_ = NumericUpDown()
        self.SqrSide_.DecimalPlaces = 2
        self.SqrSide_.Increment = 0.01
        self.SqrSide_.MaxValue = 30
        self.SqrSide_.MinValue = 5
        self.SqrSide_.Value = 10
        
        self.TopArcFactor_ = NumericUpDown()
        self.TopArcFactor_.DecimalPlaces = 2
        self.TopArcFactor_.Increment = 0.01
        self.TopArcFactor_.MaxValue = 30
        self.TopArcFactor_.MinValue = 0.1
        self.TopArcFactor_.Value = 1

        self.Border_ = NumericUpDown()
        self.Border_.DecimalPlaces = 2
        self.Border_.Increment = 0.01
        self.Border_.MaxValue = 10.0
        self.Border_.MinValue = 0
        self.Border_.Value = 1

        self.Depth_ = NumericUpDown()
        self.Depth_.DecimalPlaces = 2
        self.Depth_.Increment = 0.01
        self.Depth_.MaxValue = 10
        self.Depth_.MinValue = 0
        self.Depth_.Value = 1

        self.TopThickness_ = NumericUpDown()
        self.TopThickness_.DecimalPlaces = 2
        self.TopThickness_.Increment = 0.01
        self.TopThickness_.MaxValue = 10.0
        self.TopThickness_.MinValue = 0.5
        self.TopThickness_.Value = 3

        self.SideArcFactor_ = NumericUpDown()
        self.SideArcFactor_.DecimalPlaces = 2
        self.SideArcFactor_.Increment = 0.01
        self.SideArcFactor_.MaxValue = 30
        self.SideArcFactor_.MinValue = 0.1
        self.SideArcFactor_.Value = 0.7

        self.BottomAndSideThickness_ = NumericUpDown()
        self.BottomAndSideThickness_.DecimalPlaces = 2
        self.BottomAndSideThickness_.Increment = 0.01
        self.BottomAndSideThickness_.MaxValue = 10.0
        self.BottomAndSideThickness_.MinValue = 0.5
        self.BottomAndSideThickness_.Value = 1

        self.BottomArcFactor_ = NumericUpDown()
        self.BottomArcFactor_.DecimalPlaces = 2
        self.BottomArcFactor_.Increment = 0.01
        self.BottomArcFactor_.MaxValue = 30
        self.BottomArcFactor_.MinValue = 0.1
        self.BottomArcFactor_.Value = 0.5
        
        self.BottomWidth_ = NumericUpDown()
        self.BottomWidth_.DecimalPlaces = 2
        self.BottomWidth_.Increment = 0.01
        self.BottomWidth_.MaxValue = 30
        self.BottomWidth_.MinValue = 1
        self.BottomWidth_.Value = 3

        # Create table layout
        layout = TableLayout()
        layout.Spacing = Size(5, 5)
        layout.Rows.Add(TableRow(label0, self.RingSize_))
        layout.Rows.Add(TableRow(label1, self.SqrSide_))
        layout.Rows.Add(TableRow(label2, self.TopArcFactor_))
        layout.Rows.Add(TableRow(label3, self.Border_))
        layout.Rows.Add(TableRow(label4, self.Depth_))
        layout.Rows.Add(TableRow(label5, self.TopThickness_))
        layout.Rows.Add(TableRow(label6, self.SideArcFactor_))
        layout.Rows.Add(TableRow(label7, self.BottomAndSideThickness_))
        layout.Rows.Add(TableRow(label8, self.BottomArcFactor_))
        layout.Rows.Add(TableRow(label9, self.BottomWidth_))

        return layout
    
    # Creates checkbox controls
    def CreateCheckBoxes(self):
        # Create checkboxes
        self.CutWindow_ = CheckBox(
            Text = 'Cut window', 
            Checked = self.Args.CutWindow_,
            ThreeState = False
            )
        self.FullyFilled_ = CheckBox(
            Text = 'Fully filled', 
            Checked = self.Args.FullyFilled_,
            ThreeState = False
            )
        self.MovePrevious_ = CheckBox(
            Text = 'Move previous models', 
            Checked = self.Args.MovePrevious_,
            ThreeState = False
            )
        
        # Create Radio Button List Control
        self.AxisButtonlist_ = RadioButtonList()
        self.AxisButtonlist_.DataStore = ['x', 'y', 'z']
        self.AxisButtonlist_.Orientation = Orientation.Horizontal

        # Create table layout
        layout = DynamicLayout()
        layout.Spacing = Size(5, 5)
        layout.Rows.Add(self.CutWindow_)
        layout.Rows.Add(self.FullyFilled_)
        layout.Rows.Add(None) # spacer
        layout.Rows.Add(None) # spacer
        layout.Rows.Add(None) # spacer
        layout.Rows.Add(self.MovePrevious_)
        layout.Rows.Add(self.AxisButtonlist_)
        return layout
    
    # OK button click handler
    def OnOkButtonClick(self, sender, e):
        # Harvest control values before closing
        self.Args.RingSize_ = self.RingSize_.Value
        self.Args.SqrSide_ = self.SqrSide_.Value
        self.Args.TopArcFactor_ = self.TopArcFactor_.Value
        self.Args.Border_ = self.Border_.Value
        self.Args.Depth_ = self.Depth_.Value
        self.Args.TopThickness_ = self.TopThickness_.Value
        self.Args.SideArcFactor_ = self.SideArcFactor_.Value
        self.Args.BottomAndSideThickness_ = self.BottomAndSideThickness_.Value
        self.Args.BottomArcFactor_ = self.BottomArcFactor_.Value
        self.Args.BottomWidth_ = self.BottomWidth_.Value
        self.Args.CutWindow_ = self.CutWindow_.Checked
        self.Args.FullyFilled_ = self.FullyFilled_.Checked
        self.Args.MovePrevious_ = self.MovePrevious_.Checked
        self.Args.AxisButtonlist_ = self.AxisButtonlist_.SelectedIndex
        self.Close(True)
    
    # Cancel button click handler
    def OnCancelButtonClick(self, sender, e):
        self.Close(False)
    
    # Create button controls
    def CreateButtons(self):
        # Create the default button
        self.DefaultButton = Button(Text = 'OK')
        self.DefaultButton.Click += self.OnOkButtonClick
        # Create the abort button
        self.AbortButton = Button(Text = 'Cancel')
        self.AbortButton.Click += self.OnCancelButtonClick
        # Create button layout
        button_layout = TableLayout()
        button_layout.Spacing = Size(5, 5)
        button_layout.Rows.Add(TableRow(None, self.DefaultButton, self.AbortButton, None))
        return button_layout
    
class BuildScript():

    def __init__(self, args):
        self.Args = args
            
    def perform(self):

        ringSize = self.Args.RingSize_
        sqrSide = self.Args.SqrSide_
        arcFactor = self.Args.TopArcFactor_
        border = self.Args.Border_
        depth = self.Args.Depth_
        topThickness = self.Args.TopThickness_
        sideArcFactor = self.Args.SideArcFactor_
        bottomAndSideThickness = self.Args.BottomAndSideThickness_
        bottomArcFactor = self.Args.BottomArcFactor_
        bottomWidth = self.Args.BottomWidth_
        cutWindow = self.Args.CutWindow_
        fullyFilled = self.Args.FullyFilled_
        movePrevious = self.Args.MovePrevious_
        axisMove = self.Args.AxisButtonlist_

        topZPoint = ringSize / 2 + topThickness
        bottomZPoint1 = -(ringSize / 2) - bottomAndSideThickness
        bottomZPoint2 = -(ringSize / 2) - bottomAndSideThickness - bottomArcFactor
        sideXPoint1 = ringSize / 2 + bottomAndSideThickness
        sideXPoint2 = ringSize / 2 + bottomAndSideThickness + sideArcFactor

        ZX = rs.WorldZXPlane()
        XY = rs.WorldXYPlane()

        if(movePrevious == True):
            allObjs = rs.AllObjects( select=False, include_lights=False, include_grips=False, include_references=False ) 
            if(allObjs != None):
                if axisMove == 0:
                    rs.MoveObjects( allObjs, [(ringSize + bottomAndSideThickness)*1.33, 0, 0] )
                elif axisMove == 1:
                    rs.MoveObjects( allObjs, [0, sqrSide*1.33, 0] )
                elif axisMove == 2:
                    rs.MoveObjects( allObjs, [0, 0, sqrSide*1.5] )
                else:
                    rs.MoveObjects( allObjs, [0, sqrSide*1.33, 0] )

        baseCircle = rs.AddCircle( ZX, ringSize/2 )
        centralLine = rs.AddLine( (0,0,0), (0,50,0) )

        arc3pnt1 = rs.AddArc3Pt( (sqrSide/2, -sqrSide/2, topZPoint), (sqrSide/2, sqrSide/2, topZPoint), (sqrSide / 2 + arcFactor, 0, topZPoint) )
        arc3pnt2 = rs.RotateObject(arc3pnt1, (0,0,0), 90.0, (0,0,1), copy=True)
        arc3pnt3 = rs.RotateObject(arc3pnt1, (0,0,0), 180.0, (0,0,1), copy=True)
        arc3pnt4 = rs.RotateObject(arc3pnt1, (0,0,0), -90, (0,0,1), copy=True)

        topShortLine1 = rs.AddLine((sqrSide / 2 + arcFactor,0,topZPoint), (sqrSide / 2 + arcFactor,0,topZPoint+2))
        topShortLine2 = rs.RotateObject(topShortLine1, (0,0,0), 90.0, (0,0,1), copy=True)

        bottomArc3pnt = rs.AddArc3Pt( (0, -bottomWidth/2, bottomZPoint1), (0, bottomWidth/2, bottomZPoint1), (0, 0, bottomZPoint2) )

        bottomArc = rs.AddArc3Pt( (sideXPoint2, 0, 0), (-sideXPoint2, 0, 0), (0, 0, bottomZPoint2) )

        domain_crv0 = rs.CurveDomain( topShortLine1 )
        domain_crv1 = rs.CurveDomain( bottomArc )
        params = domain_crv0[0], domain_crv1[0]
        revs = False, True
        cont = 0,2
        bl1 = rs.AddBlendCurve( (topShortLine1, bottomArc), params, revs, cont )

        domain_crv0 = rs.CurveDomain( topShortLine2 )
        domain_crv1 = rs.CurveDomain( bottomArc3pnt )
        params = domain_crv0[0], domain_crv1[1]
        revs = True, False
        cont = 1,0
        bl2 = rs.AddBlendCurve( (topShortLine2, bottomArc3pnt), params, revs, cont )

        rail = rs.JoinCurves( (bl1, bottomArc), True )
        surf1 = rs.AddSweep1(rail, (arc3pnt1, bottomArc3pnt), closed=False)

        domain = rs.CurveDomain(arc3pnt2)
        parameter = domain[1] / 2.0
        split = rs.SplitCurve( arc3pnt2, parameter, delete_input=False )

        borders = rs.DuplicateEdgeCurves( surf1, select=True )

        surf2 = rs.AddEdgeSrf( [split[0], borders[2], bl2] )
        surf3 = rs.MirrorObject( surf2, (0,0,0), (1,0,0), True )
        surf4 = rs.JoinSurfaces([surf1, surf2, surf3], delete_input=True)
        surf5 = rs.MirrorObject( surf4, (0,0,0), (0,1,0), True )
        surf6 = rs.JoinSurfaces([surf4, surf5], delete_input=True)
        rs.CapPlanarHoles(surf6)

        cylinder = rs.ExtrudeCurve( baseCircle, centralLine )
        rs.MoveObject( cylinder, [0,-25,0] )
        rs.CapPlanarHoles( cylinder )
        solidRing = rs.BooleanDifference( surf6, cylinder, True )

        if(fullyFilled == False):
            xform = rs.XformScale( (0.9, 0.8, 1-topThickness/topZPoint) )
            solid = rs.TransformObjects( solidRing, xform, True )
            move = [ 0,0,(topThickness - depth) / 2 ]
            solid = rs.MoveObjects( solid, move )
            solidRing = rs.BooleanDifference( solidRing, solid, delete_input=True )

        if (cutWindow == True):
            topCurve = rs.JoinCurves( (arc3pnt1, arc3pnt2, arc3pnt3, arc3pnt4), True )
            offsCur = rs.OffsetCurve( topCurve, [0,0,topZPoint], border )
            extrudePath2 = rs.AddLine( (0,0,0), (0,0,-depth) )
            cuttingObject = rs.ExtrudeCurve( offsCur, extrudePath2 )
            rs.CapPlanarHoles( cuttingObject )
            solidRing = rs.BooleanDifference( solidRing, cuttingObject, True )
        
        curves = rs.ObjectsByType(4, False)
        rs.DeleteObjects(curves)


def Run():
    args = BuildArgs()
    dlg = BuildDialog(args)
    buildScript = BuildScript(args)
    modal = dlg.ShowModal(RhinoEtoApp.MainWindow)
    if modal and args.IsValid():
        buildScript.perform()
        
if __name__ == "__main__":
    Run()