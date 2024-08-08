import React from "react";
import escapeRegExp from "./escapeRegExp";


export default function Suggestion({ check, setGenerateSuggestions, setTextInput }) {
    const handleSuggestionClick = (event) => {
        event.preventDefault();
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
            {/* Word */}
            <div className="d-flex mb-2">
                <span>{check.token}</span>
            </div>

            {check.suggestions && (
                <div className="d-flex mb-2">
                    {/* Replace options */}
                    <select className="replace-mode form-select form-select-sm me-auto" style={{maxWidth: "110px", fontSize: "small"}}>
                        <option value="replace">Replace</option>
                        <option value="replace-all">Replace all</option>
                    </select>

                    {/* Suggestions items */}
                    <div>
                        {check.suggestions.map((suggestion, i) => (
                            <button
                                key={i}
                                className="suggestion btn btn-sm border me-1"
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