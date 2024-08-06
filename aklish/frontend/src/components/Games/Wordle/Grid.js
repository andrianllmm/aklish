import React from "react";
import Row from "./Row";


export default function Grid({ solutionLen, currentGuess, guesses, turn }) {
    return (
        <div className="grid">
            {guesses.map((g, i) => {
                if (turn === i) {
                    return <Row key={i} len={solutionLen} currentGuess={currentGuess}/>
                }
                return <Row key={i} len={solutionLen} guess={g}/>
            })}
        </div>
    )
}
