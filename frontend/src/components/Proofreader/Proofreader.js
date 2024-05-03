import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import Header from "../Header";
import Suggestion from "./Suggestion";
import TextField from "./TextField";
import escapeRegExp from "./escapeRegExp";


export default function Proofreader() {
    const [lang, setLang] = React.useState(useParams().lang);
    const [textInput, setTextInput] = useState("");
    const [textMarks, setTextMarks] = useState("");
    const [suggestions, setSuggestions] = useState([]);
    const [wordCount, setWordCount] = useState(0);
    const [mistakeCount, setMistakeCount] = useState(0);
    const [correctness, setCorrectness] = useState("");
    const [showSuggestions, setShowSuggestions] = useState(true);
    const [generateSuggestions, setGenerateSuggestions] = useState(false);

    useEffect(() => {
        if (textInput.trim().length > 0) {
            fetch(`/proofreader/api/${lang}/?text=${textInput}`)
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
        } else {
            setSuggestions(["Start typing to get suggestions."]);
        }
    }, [generateSuggestions, lang]);

    useEffect(() => {
        if (textInput.trim().length > 0) {
            fetch(`/proofreader/api/${lang}/?text=${textInput}`)
                .then(response => response.json())
                .then(data => {
                    console.log(data.checks.filter(Boolean))
                    setWordCount(data.checks.filter(Boolean).length);
                    let mistakes = 0;
                    data.checks.forEach(check => {
                        if (!check.valid) {
                            mistakes++;
                        }
                    });
                    setMistakeCount(mistakes);

                })
        } else {
            setWordCount(0);
            setMistakeCount(0);
        }
    }, [textInput, lang]);

    useEffect(() => {
        if (textInput.trim().length > 0) {
            fetch(`/proofreader/api/${lang}/?text=${textInput}`)
                .then(response => response.json())
                .then(data => {
                    let markedText = textInput;
                    data.checks.forEach(check => {
                        if (!check.valid) {
                            markedText = markedText.replace(new RegExp(`\\b${escapeRegExp(check.token)}\\b(?!</u>)`, "g"), `<u class="mispelled">${check.token}</u>`);
                        }
                    });
                    setTextMarks(markedText);
                })
        } else {
            setTextMarks("");
        }
    }, [wordCount, lang]);

    useEffect(() => {
        if (parseInt(wordCount) === 0) {
            setCorrectness("%");
        } else if (parseInt(mistakeCount) === 0) {
            setCorrectness("100%");
        } else {
            const correctnessPercentage = Math.round(100 * (1 - (parseInt(mistakeCount) / parseInt(wordCount)))) + "%";
            setCorrectness(correctnessPercentage);
        }
    }, [wordCount, mistakeCount]);

    const handleInputChange = (event) => {
        setTextInput(event.target.value);
        setSuggestions(["Typing..."])
    };

    const handleGenerateSuggestions = () => {
        setGenerateSuggestions(prev => !prev);
        setShowSuggestions(true);
    };

    const toggleSuggestions = () => {
        setShowSuggestions(prev => !prev);
    };

    return (
        <>
            <Header title="Proofreader" />
            <div className="container mb-3">
                <div className="row mb-2">
                    <div className="col p-0">
                        <TextField textInput={textInput} textMarks={textMarks} handleInputChange={handleInputChange}/>
                    </div>
                    <div id="proofreader-suggestions-col" className={`col p-0 ms-3 ${showSuggestions ? "" : "d-none"}`}>
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
                <div className="d-flex align-items-center">
                    <div className="me-auto">
                        <small className="me-2">
                            <strong id="word-count">{wordCount}</strong> words
                        </small>
                        <small className="me-2">
                            <strong id="mistake-count">{mistakeCount}</strong> mistakes
                        </small>
                        <small>
                            <strong id="correctness">{correctness}</strong> correct
                        </small>
                    </div>
                    <div>
                        <button id="toggle-suggestions" className="btn" onClick={toggleSuggestions}>
                            <i className={showSuggestions ? "bi bi-eye-slash" : "bi bi-eye"}></i>
                        </button>
                        <button id="generate-suggestions" className="btn btn-outline-secondary me-2" onClick={handleGenerateSuggestions}>
                            <i className="bi bi-spellcheck"></i> <small>Proofread</small>
                        </button>
                    </div>
                </div>
            </div>
        </>
    );
}