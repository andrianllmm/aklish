import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom/client";
import { useParams } from "react-router-dom";
import Suggestion from "./Suggestion";
import TextField from "./TextField";
import escapeRegExp from "./escapeRegExp";


export default function ProofreaderField({ defaultShowSuggestions }) {
    const [lang, setLang] = React.useState(useParams().lang);
    const [textInput, setTextInput] = useState(localStorage.getItem("proofreaderTextInput") || "");
    const [textMarks, setTextMarks] = useState("");
    const [suggestions, setSuggestions] = useState([]);
    const [tokenCount, setTokenCount] = useState(0);
    const [wordCount, setWordCount] = useState(0);
    const [mistakeCount, setMistakeCount] = useState(0);
    const [correctness, setCorrectness] = useState(null);
    const [whiteSpaceCount, setWhiteSpaceCount] = useState(0);
    const [showSuggestions, setShowSuggestions] = useState(defaultShowSuggestions || false);
    const [generateSuggestions, setGenerateSuggestions] = useState(false);
    const fetchUrl = `/proofreader/api/${lang}/?text=${textInput}`;

    const langSelect = document.querySelector("#lang");
    if (langSelect) {
        langSelect.addEventListener("change", (event) => {
            setLang(event.target.value);
        })
    }

    useEffect(() => {
        if (langSelect) {
            setLang(langSelect.value);
        }
        if (!lang) {
            setLang("akl");
        }
    }, [lang]);

    useEffect(() => {
        localStorage.setItem("proofreaderTextInput", textInput);
    }, [textInput])

    useEffect(() => {
        if (textInput.trim().length > 0) {
            fetch(fetchUrl)
                .then(response => response.json())
                .then(data => {
                    setTokenCount(data.checks.filter(Boolean).length);
                    setWordCount(data.word_count);
                    setMistakeCount(data.mistake_count);
                    setCorrectness(data.correctness);
                })
                .catch(error => {
                    console.error("Error fetching data: ", error);
                });
        } else {
            setWordCount(0);
            setMistakeCount(0);
            setCorrectness(null);
            setTextMarks("");
        }
    }, [textInput, lang]);

    useEffect(() => {
        if (textInput.trim().length > 0) {
            fetch(fetchUrl)
                .then(response => response.json())
                .then(data => {
                    let markedText = textInput;
                    data.checks.forEach(check => {
                        if (!check.valid) {
                            markedText = markedText.replace(
                                new RegExp(`\\b${escapeRegExp(check.token)}\\b(?!</u>)`, "g"),
                                `<u class="mispelled">${check.token}</u>`
                            );
                        }
                    });
                    setTextMarks(markedText);
                })
                .catch(error => {
                    console.error("Error fetching data: ", error);
                });
        } else {
            setTextMarks("");
        }
    }, [whiteSpaceCount, generateSuggestions, lang]);

    useEffect(() => {
        if (textInput.trim().length > 0) {
            fetch(fetchUrl)
                .then(response => response.json())
                .then(data => {
                    let generatedSuggestions = data.checks.map((check, i) => {
                        if (!check.valid) {
                            return (
                                <Suggestion check={check} key={i}
                                setGenerateSuggestions={setGenerateSuggestions}
                                setTextInput={setTextInput}/>
                            );
                        }
                        return null;
                    });
                    let filteredSuggestions = generatedSuggestions.filter(Boolean)
                    setSuggestions(filteredSuggestions);
                    
                    if (filteredSuggestions.length === 0) {
                        setSuggestions(["No mistakes found."]);
                    }
                })
                .catch(error => {
                    console.error("Error fetching data: ", error);
                });
        } else {
            setSuggestions(["Start typing to get suggestions."]);
        }
    }, [generateSuggestions, lang]);

    const handleInputChange = (event) => {
        const value = event.target.value;
        setTextInput(value);
        setWhiteSpaceCount(value.split(" ").length - 1);
        setSuggestions(["Typing..."])
    };

    const handleGenerateSuggestions = (event) => {
        event.preventDefault();
        setGenerateSuggestions(prev => !prev);
        setShowSuggestions(true);
    };

    const toggleSuggestions = (event) => {
        event.preventDefault();
        setShowSuggestions(prev => !prev);
    };

    return (
        <div className="container mb-3">
            <div className="row mb-2">
                <div className="col-md p-0 m-1 ">
                    <TextField textInput={textInput} textMarks={textMarks} handleInputChange={handleInputChange}/>
                </div>
                <div id="proofreader-suggestions-col" className={`col-md p-0 m-1 ${showSuggestions ? "" : "d-none"}`}>
                    <div>
                        <h5>Suggestions</h5>
                    </div>
                    <div>
                        <ul id="proofreader-suggestions" className="list-group">
                            {suggestions}
                        </ul>
                    </div>
                </div>
            </div>
            <div className="d-flex align-items-center p-1 border-top border-bottom">
                <div className="d-flex flex-wrap me-auto">
                    <small className="me-2 text-nowrap">
                        <strong id="word-count">{wordCount}</strong> words
                    </small>
                    <small className="me-2 text-nowrap">
                        <strong id="mistake-count">{mistakeCount}</strong> mistakes
                    </small>
                    <small className="me-2 text-nowrap">
                        <strong id="correctness">{correctness}%</strong> correct
                    </small>
                </div>
                <div>
                    <button id="toggle-suggestions" className="btn px-2 py-1" onClick={toggleSuggestions}>
                        <i className={showSuggestions ? "bi bi-eye-slash" : "bi bi-eye"}></i>
                    </button>
                    <button id="generate-suggestions" className="btn px-2 py-1" onClick={handleGenerateSuggestions}>
                        <i className="bi bi-spellcheck"></i>
                    </button>
                </div>
            </div>
        </div>
    );
}

window.addEventListener("DOMContentLoaded", function (event) {
    ReactDOM.createRoot(
        document.querySelector("#proofreader-field")
    )
    .render(
        <ProofreaderField />
    );
})