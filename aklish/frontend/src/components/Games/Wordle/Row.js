import React from "react";


export default function Row({ len, guess, currentGuess }) {
    if (guess) {
        return (
            <div className="row past">
                {guess.map((char, i) => {
                    return <div key={i} className={char.status}>{char.key}</div>
                })}
            </div>
        )
    }

    if (currentGuess) {
        let chars = currentGuess.split("");

        return (
            <div className="row current">
                {chars.map((char, i) => {
                    return <div key={i} className="filled">{char}</div>
                })}
                {[...Array(len - chars.length)].map((_, i) => {
                    return <div key={i}></div>
                })}
            </div>
        )
    }

    return (
        <div className="row">
            {[...Array(len)].map((_, i) => {
                return <div key={i}></div>
            })}
        </div>
    )
}
