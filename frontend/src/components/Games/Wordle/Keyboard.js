import React from 'react';

export default function Keyboard({handleKeyup}) {
    const [keys, setKeys] = React.useState([
        [..."QWERTYUIOP"],
        [..."-ASDFGHJKL'"],
        ["Backspace", ..."ZXCVBNM", "Enter"]
    ]);

    return (
        <div className="keyboard">
            {keys && keys.map((row, i) => (
                <div className="row" key={i}>
                    {row.map((key, j) => (
                        <div className="col m-1 p-0" key={j}>
                            <button
                            className="key btn btn-secondary"
                            onClick={() => handleKeyup({ key })}
                            >
                                {key}
                            </button>
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );
}
