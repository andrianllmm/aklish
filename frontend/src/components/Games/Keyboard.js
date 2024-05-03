import React from 'react';


export default function Keyboard({handleKeyup}) {
    const [keys, setKeys] = React.useState([
        [..."QWERTYUIOP"],
        [..."-ASDFGHJKL'"],
        ["Enter", ..."ZXCVBNM", "Backspace"]
    ]);

    return (
        <div className="keyboard">
            {keys && keys.map((row, i) => (
                <div className="row my-1" key={i}>
                    {row.map((key, j) => (
                        <button
                        value={key}
                        className="key col btn btn-secondary p-1 mx-1"
                        onClick={() => handleKeyup({ key })}
                        key={j}
                        >
                            {key === "Backspace" ? (
                                <i className="bi bi-backspace"></i>
                            ) : key === "Enter" ? (
                                <i className="bi bi-arrow-return-left"></i>
                            ) : (
                                key
                            )}
                        </button>
                    ))}
                </div>
            ))}
        </div>
    );
}
