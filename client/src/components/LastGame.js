import React from 'react';
import { useState, useEffect } from 'react';
import ReactHtmlParser from 'react-html-parser';

export default function LastGame() {
    const [lastGame, setLastGame] = useState("");
    const [lastGameOpponent, setLastGameOpponent] = useState("");
    useEffect(() => {
      fetch("/last-game").then(
        res => res.json()
      ).then(
        data => {
            setLastGame([data.last_game])
            setLastGameOpponent([data.last_game_opponent])
        }
      )
    }, []);
    if (lastGame == "" || lastGameOpponent == "") {
      return <></>;
    }
    return (
      <div className="lastGame">
        <p>Warriors Stats</p>
        <div style={{left: "200px"}}>{ ReactHtmlParser(lastGame) }</div>
        <p>Opponent Stats</p>
        { ReactHtmlParser(lastGameOpponent) }
      </div>
    );
}
