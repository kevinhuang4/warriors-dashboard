import React from 'react';
import { useState, useEffect } from 'react';

export default function Recent() {
  const [recentGames, setRecentGames] = useState(null);
  useEffect(() => {
    fetch("/recent").then(
      res => res.json()
    ).then(
      data => {
        // console.log(data);
        setRecentGames([data.last_game, data.next_game])
      }
    )
  }, []);
  if (recentGames == null) {
    return <></>;
  }
  return (
    <div className="recent">
      <p>Last Game: {recentGames[0]}</p>
      <p>Next Game: {recentGames[1]}</p>
    </div>
  );
}
