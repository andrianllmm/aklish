import React from "react";
import escapeRegExp from "./escapeRegExp";


export default function Suggestion({ check, setGenerateSuggestions, setTextInput }) {
    const handleSuggestionClick = (event) => {
        const changefrom = event.target.getAttribute("data-changefrom");
        const changeto = event.target.getAttribute("data-changeto");
        const replaceMode = event.target.parentNode.parentNode.querySelector(".replace-mode").value;

        if (replaceMode === "replace") {
            setTextInput(prev => prev.replace(new RegExp(`\\b${escapeRegExp(changefrom)}\\b`), changeto));
        } else if (replaceMode === "replace-all") {
            setTextInput(prev => prev.replace(new RegExp(`\\b${escapeRegExp(changefrom)}\\b`, "g"), changeto));
        }

        setGenerateSuggestions(prev => !prev);
    }

    return (
        <li className="list-group-item">
            <div className="d-flex mb-2">
                <u style={{ textDecorationColor: "red" }}>{check.token}</u>
            </div>
            {check.suggestions && (
                <div className="d-flex mb-2">
                    <select className="replace-mode form-select form-select-sm me-auto" style={{ width: "150px" }}>
                        <option value="replace">Replace</option>
                        <option value="replace-all">Replace all</option>
                    </select>
                    <div>
                        {check.suggestions.map((suggestion, i) => (
                            <button
                                key={i}
                                className="suggestion btn btn-sm btn-secondary me-1"
                                data-changefrom={check.token}
                                data-changeto={suggestion}
                                onClick={handleSuggestionClick}
                            >
                                {suggestion}
                            </button>
                        ))}
                    </div>
                </div>
            )}
        </li>
    )
}