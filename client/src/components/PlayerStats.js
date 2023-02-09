import React from 'react';
import { useState, useEffect } from 'react';
import ReactHtmlParser from 'react-html-parser';

export default function PlayerStats() {
    const [stats, setStats] = useState("");
    useEffect(() => {
      fetch("/player-stats").then(
        res => res.json()
      ).then(
        data => {
        //   console.log(data);
          setStats(data.player_stats)
        }
      )
    }, []);
    if (stats == "") {
      return <></>;
    }
    return (
      <div className="recent">
        <p>Player Stats</p>
        { ReactHtmlParser(stats) }
      </div>
    );
}
