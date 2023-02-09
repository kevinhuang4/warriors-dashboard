import React from 'react';
import { useState, useEffect } from 'react';

export default function Standings() {
  const [fetched, setFetched] = useState(false);
  const [standing, setStanding] = useState("");
  const [wl, setWl]  = useState("");
  const [rankings, setRankings]  = useState([]);
  useEffect(() => {
    fetch("/standings").then(
      res => res.json()
    ).then(
      data => {
        if (data) {
          // console.log(data);
          setFetched(true);
          setStanding(data.standing);
          setWl(data.wl);
          let zipped = data.rankings.map(
            (ranking, i) => [ranking + "th " + data.ranking_titles[i], data.ranking_numbers[i] + " " + data.ranking_units[i]]
          );
          setRankings(zipped);
        }
      }
    )
  }, []);
  if (fetched == false) {
    return <>Still loading...</>;
  }
  return (
    <div className="standing">
      <p>Warriors are currently ranked</p>
      <h1>{standing}</h1>
      <p>in the Western Conferenece ({wl})</p>
      {rankings.map(function(ranking, index){
        return <p key={ index }>{ranking[0] + " " + ranking[1]}</p>;
      })}
    </div>
  );
}
