import React, { useRef, useEffect, useState } from 'react'

function App () {

  const [readText, setText] = useState("write using the mouse pointer in the space below");

  const canvasRef = useRef(null);
  const contextRef = useRef(null);

  //Bezier midpoints and tracker
  const [cp1x, setCp1x] = useState(0);
  const [cp1y, setCp1y] = useState(0);
  const [cp2x, setCp2x] = useState(0);
  const [cp2y, setCp2y] = useState(0);
  const [bezierCnt, setBezierCnt] = useState(0);

  const placePen = ({ nativeEvent }) => {
    const { offsetX, offsetY } = nativeEvent;
    contextRef.current.beginPath();
    contextRef.current.moveTo(offsetX, offsetY);
    setBezierCnt(1);
  };

  const completeBeziers = ({ nativeEvent }) => {

    const context = contextRef.current;

    const { offsetX, offsetY } = nativeEvent;

    if (bezierCnt == 0){
      return;
    } else if(bezierCnt == 1){
      setCp1x(offsetX);
      setCp1y(offsetY);
      setBezierCnt(2);
    } else if (bezierCnt == 2){
      setCp2x(offsetX);
      setCp2y(offsetY);
      setBezierCnt(3);
    } else if (bezierCnt == 3){
      context.bezierCurveTo(cp1x, cp1y, cp2x, cp2y, offsetX, offsetY);
      context.lineWidth = 5
      context.stroke();
      
      setBezierCnt(1);
      context.beginPath();
      context.moveTo(offsetX, offsetY);
    }
  };

  const liftPen = () => {
    const context = contextRef.current;

    context.closePath();
    setBezierCnt(0);
  };

  useEffect(() => {
    const canvas = canvasRef.current

    canvas.setAttribute("width", `${window.innerWidth * 2 * 0.95}`);
    canvas.setAttribute("height", `${window.innerHeight * 2 * 0.85}`);
    canvas.style.width = `${(window.innerWidth)*0.95}px`;
    canvas.style.height = `${(window.innerHeight)*0.85}px`;

    const context = canvas.getContext("2d");
    contextRef.current = context;

    context.fillStyle = "#ffffff";
    context.fillRect(0, 0, canvas.width, canvas.height);
    context.strokeStyle="#000000";
    context.lineWidth = 5;
    context.strokeRect(0, 0, canvas.width, canvas.height);

    context.scale(2, 2);
  
  }, [])

  const newScreen = () => {
    const context = contextRef.current;
    const canvas = canvasRef.current;

    canvas.setAttribute("width", `${window.innerWidth * 2 * 0.95}`);
    canvas.setAttribute("height", `${window.innerHeight * 2 * 0.85}`);
    canvas.style.width = `${(window.innerWidth)*0.95}px`;
    canvas.style.height = `${(window.innerHeight)*0.85}px`;

    context.fillStyle = "#ffffff";
    context.fillRect(0, 0, canvas.width, canvas.height);
    context.strokeStyle="#000000";
    context.lineWidth = 5;
    context.strokeRect(0, 0, canvas.width, canvas.height);

    context.scale(2, 2);
  }

  const saveImage = () => {

    var anchor = document.createElement("a");
    anchor.download = "savedHandwriting.png";

    const canvas = canvasRef.current;
    var anchorHref = canvas.toDataURL("image/png");
    anchor.href=anchorHref;

    document.body.appendChild(anchor);
    anchor.click();
  }

  const processText = () => {

    const canvas = canvasRef.current;
    var imgURL = canvas.toDataURL();
    console.log(imgURL);

    fetch("/process", {
      method: 'PUT',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        pngBase64: imgURL,
        upjson: 'default text'
      })
    }).then( () => {

      fetch("/process").then(getresponse => {
        if(getresponse.status == 200){
          return getresponse.json()
        }
      }).then( getData => setText( getData.reading ) )

    })
    
  }
  
  return( 
    <div>
      <button onClick={newScreen} >
        Wipe
      </button>
      <button onClick={saveImage}>
        Download
      </button>
      <button onClick={processText}>
        Process writing
      </button>
      <p>
        Input read as: {readText}
      </p>
      <canvas 
        onMouseDown={placePen}
        onMouseMove={completeBeziers}
        onMouseUp={liftPen}
        ref={canvasRef}
      /> 
    </div>
    );
}

export default App