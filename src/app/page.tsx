"use client";
import {useEffect, useState} from "react";
import {BASE_API_URL} from "../../utils/constants";
import macbookIphone from './detectedParkingSpot.png';

const Home: React.FC = () => {
  const [parkingMap, setParkingMap] = useState([])

    const handleDataRequest = () => {
        if (!BASE_API_URL) {
            return null;
        }
        fetch(`${BASE_API_URL}/api/getParkingMap`)
            .then(response => response.json())
            .then(data => setParkingMap(data))
    }

    // @ts-ignore
    return (
        <div>
            <h1>Home</h1>
            <button onClick={handleDataRequest}>Get Data</button>
            {parkingMap.length > 0 && (<>
                <h2> Parking Map Json Data: <i>{JSON.stringify(parkingMap) ?? "Not available"}</i></h2>
                <h2> The closest lot available is marked with yellow, other vacant lots are marked with green</h2>
                <img
                    src={macbookIphone.src}
                    width={500}
                    height={500}
                    alt="Picture of parking lot"
                />
                <h2>
                    <a href='https://itch.io/embed-upload/10453501?color=333333'> Click here for the navigation video </a>
                </h2>
            </>)}
        </div>
    );
};

export default Home;
