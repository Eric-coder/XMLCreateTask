styleData = """
QWidget
{
    color: #b1b1b1;
    background-color: #323232;
}
QProgressBar
{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center;
}
QProgressBar::chunk
{
    background-color: #d7801a;
    width: 2.15px;
    margin: 0.5px;
}
QPushButton:pressed
{
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);
}
QPushButton:hover
{
    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
    
}
QPushButton
{
    color: #b1b1b1;
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);
    border-width: 1px;
    border-color: #1e1e1e;
    border-style: solid;
    border-radius: 6;
    padding: 3px;
    font-size: 12px;
    padding-left: 5px;
    padding-right: 5px;
}
QLineEdit:enabled 
{
        color: rgb(175, 175, 175);
}

QLineEdit:focus
{

	border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
}
  
QLineEdit
{
    color: #b1b1b1;
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);
    border-width: 0.5px;
    selection-background-color: green;
    border-color: #1e1e1e;
    border-style: solid;
    border-radius: 0;
    padding: 2px;
    font-size: 12px;
    padding-left: 5px;
    padding-right: 5px;
}
QRadioButton::indicator::checked{ 
	background-color:red;
    border-radius: 1px;
	border-style: solid;
	
}  
QRadioButton
{
    /*color: green;*/
    selection-background-color: green;
}

"""
