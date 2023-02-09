import React from 'react';
import { useState, useEffect } from 'react';
import ReactHtmlParser from 'react-html-parser';

export default function Injuries() {
    const [injuries, setInjuries] = useState("");
    useEffect(() => {
      fetch("/injuries").then(
        res => res.json()
      ).then(
        data => {
        //   console.log(data);
          setInjuries(data.injuries)
        }
      )
    }, []);
    if (injuries == "") {
      return <></>;
    }
    return (
      <div className="recent">
        <p>Injuries</p>
        { ReactHtmlParser(injuries) }
      </div>
    );
}
