import React, {useState, useEffect} from "react";
function index() {
    const [parkingMap, setParkingMap] = useState([])

    useEffect(() => {
        fetch('http://localhost:3005/api/getParkingMap')
        .then(response => response.json())
        .then(data => setParkingMap(data))
    },[])
  return (
    <div>
      <h1>Home</h1>
      <h1>{parkingMap.slice(0,9)}</h1>
    </div>
  );
}

export default index;
