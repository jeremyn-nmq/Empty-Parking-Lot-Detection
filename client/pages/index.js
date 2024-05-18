import React, {useState} from "react";
function index() {
    const [parkingMap, setParkingMap] = useState([])

    const handleDataRequest = () => {
        fetch('http://localhost:3005/api/getParkingMap')
        .then(response => response.json())
        .then(data => setParkingMap(data))
    }

  return (
    <div>
      <h1>Home</h1>
      <button onClick={handleDataRequest}>Get Data</button>
        <h2> Parking Map Data: {parkingMap.slice(0,9) ?? "Not available"}</h2>
    </div>
  );
}

export default index;
