import React from "react";
import { useParams } from "react-router-dom";
import Header from "../../Header";
import Keyboard from "./Keyboard";
import Message from "../Message";
import Endgame from "./Endgame";
import Grid from "./Grid";


export default function Wordle() {
    const numGuesses = 6;
    const wordLen = [4, 6];
    const [lang, setLang] = React.useState(useParams().lang);
    const [solution, setSolution] = React.useState("");
    const [hint, setHint] = React.useState("");
    const [currentGuess, setCurrentGuess] = React.useState("");
    const [turn, setTurn] = React.useState(0);
    const [guesses, setGuesses] = React.useState([...Array(numGuesses)]);
    const [history, setHistory] = React.useState([]);
    const [isCorrect, setIsCorrect] = React.useState(false);
    const [message, setMessage] = React.useState(null);
    const [endgame, setEndgame] = React.useState(false);

    React.useEffect(() => {
        fetch(
            `/dictionary/api/${lang}/entry/?` +
            `word_len=${wordLen[0]}-${wordLen[1]}&` +
            `definition_len=3-20&` +
            `word_case=lower&` +
            `definition!^=(&` +
            `classification!=vul&` +
            `origin!=eng&`
        )
            .then(response => response.json())
            .then(data => {
                setSolution(data.word.toLowerCase());

                const attributes = data.attributes;
                const definition = attributes[Math.floor(Math.random() * attributes.length)].definition;
                setHint(definition);
            })
            .catch(error => {
                setMessage(["Too many retries. Try again later.", "warning"]);
                console.error("Error fetching data: ", error);
            });
    }, []);

    function formatGuess() {
        let solutionArray = [...solution];
        let formattedGuess = [...currentGuess].map((char) => {
            return {key: char, status: "absent"};
        });

        formattedGuess.forEach((char, i) => {
            if (solutionArray[i] === char.key) {
                formattedGuess[i].status = "correct";
                solutionArray[i] = null;
            }
        });

        formattedGuess.forEach((char, i) => {
            if (solutionArray.includes(char.key) && char.status !== "correct") {
                formattedGuess[i].status = "misplaced";
                solutionArray[solutionArray.indexOf(char.key)] = null;
            }
        });

        return formattedGuess;
    }

    function addNewGuess (formattedGuess) {
        if (currentGuess === solution) {
            setIsCorrect(true);
        }

        setGuesses((prevGuesses) => {
            let newGuesses = [...prevGuesses];
            newGuesses[turn] = formattedGuess;
            return newGuesses;
        });
        setHistory((prevHistory) => {
            return [...prevHistory, currentGuess];
        });
        setTurn((prevTurn) => {
            return prevTurn + 1;
        });
        setCurrentGuess("");
    }

    function handleKeyup({key}) {
        if (key === "Enter") {
            if (history.includes(currentGuess)) {
                setMessage(["you already tried that word", "warning"]);
                return;
            }

            if (currentGuess.length !== solution.length) {
                setMessage([`word must be ${solution.length} characters long`, "warning"]);
                return;
            }

            fetch(`/dictionary/api/${lang}/entry/?word=${currentGuess}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error("Response was not ok");
                }
                const formattedGuess = formatGuess();
                addNewGuess(formattedGuess);
            })
            .catch(error => {
                setMessage([`${currentGuess} is not in the dictionary`, "warning"]);
                return;
            });
        }

        else if (key === "Backspace") {
            if (currentGuess.length > 0) {
                setCurrentGuess((prevCurrentGuess) => {
                    return (prevCurrentGuess.slice(0, -1));
                });
            }
        }

        else if (/^[A-Za-z-']$/.test(key)) {
            if (currentGuess.length < solution.length) {
                setCurrentGuess((prevCurrentGuess) => {
                    return (prevCurrentGuess.toLowerCase() + key.toLowerCase());
                });
            }
        }
    }

    React.useEffect(() => {
        window.addEventListener("keyup", handleKeyup);

        if (isCorrect) {
            setEndgame(true);
            window.removeEventListener("keyup", handleKeyup);
        }

        if (turn >= numGuesses) {
            setEndgame(true);
            window.removeEventListener("keyup", handleKeyup);
        }

        return () => {
            window.removeEventListener("keyup", handleKeyup);
        };
    }, [handleKeyup]);

    React.useEffect(() => {
        if (message) {
            const timer = setTimeout(() => {
                setMessage(null);
            }, 1500);

            return () => clearTimeout(timer);
        }
    }, [message]);

    return (
        <>
            {solution && (
                <>
                    <Header title="Wordle" />

                    <div className="container pb-2 mb-2 text-center border-bottom">
                        {/* Hint */}
                        <div>
                            <p className="m-2">Hint: <strong>{hint}</strong></p>
                        </div>

                        {/* Message */}
                        {message &&
                            <div className="d-flex justify-content-center">
                                <Message message={message[0]} variant={message[1]}/>
                            </div>
                        }

                        {/* Grid */}
                        <Grid solutionLen={solution.length} currentGuess={currentGuess} guesses={guesses} turn={turn}></Grid>

                        {/* Keyboard */}
                        <Keyboard handleKeyup={handleKeyup}></Keyboard>
                        {endgame && (
                            <Endgame show={endgame}
                                isCorrect={isCorrect}
                                solution={solution}
                                turn={turn}
                                numGuesses={numGuesses}
                            />
                        )}
                    </div>

                    {/* Guide */}
                    <div class="container d-flex">
                        <a href="/help/wordle_guide" class="link-unstyled ms-auto">
                            <i class="bi bi-question-circle me-2"></i>
                            <small>How to play</small>
                        </a>
                    </div>
                </>
            )}
        </>
    )
}
