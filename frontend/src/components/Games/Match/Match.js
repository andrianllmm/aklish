import React from "react";
import { useParams } from "react-router-dom";
import Header from "../../Header";
import Message from "../Message";
import Choices from "./Choices";
import Button from "react-bootstrap/Button";


export default function Match() {
    const modes = ["similar", "opposite"];
 
    const wordLen = [3, 10];
    const [lang, setLang] = React.useState(useParams().lang);
    const [mode, setMode] = React.useState(modes[Math.floor(Math.random() * modes.length)]);
    const [word, setWord] = React.useState("");
    const [matchWord, setMatchWord] = React.useState("");
    const [choices, setChoices] = React.useState([]);
    const [selectedChoice, setSelectedChoice] = React.useState(null);
    const [choicesReady, setChoicesReady] = React.useState(false);
    const [isCorrect, setIsCorrect] = React.useState(null);
    const [answerSelected, setAnswerSelected] = React.useState(false);
    const [message, setMessage] = React.useState(null);
    const [endgame, setEndgame] = React.useState(false);

    React.useEffect(() => {
        fetch(
            `/dictionary/api/${lang}/entry/?` + 
            `has=${mode}&` +
            `word_len=${wordLen[0]}-${wordLen[1]}&` +
            `word_case=lower&` +
            `classification!=vul&`
        )
            .then(response => response.json())
            .then(data => {
                if (data) {
                    setWord(data.word.toLowerCase());

                    const attributes = data.attributes;
                    let match_list = [];
                    for (const attribute of attributes) {
                        switch (mode) {
                            case "similar":
                                match_list.push(...attribute.similar);
                                break;
                            case "opposite":
                                match_list.push(...attribute.opposite);
                                break;
                        }
                    }
                    match_list = match_list.filter(Boolean);
                    const match_word = match_list[Math.floor(Math.random() * match_list.length)];
                    setMatchWord(match_word.toLowerCase());
                }
            })
            .catch(error => {
                if (error.response && error.response.status == 403) {
                    setMessage(["Too many retries. Try again later.", "warning"]);
                }
                console.error("Error fetching data: ", error);
            });
    }, []);

    React.useEffect(() => {
        fetch(
            `/dictionary/api/${lang}/entries/?` +
            `word!=${word}&` +
            `num=3&` +
            `levenshtein=${matchWord}&` +
            `distance=5&`
        )
            .then(response => response.json())
            .then(data => {
                let fetched_choices = [];
                if (data) {
                    for (let entry of data) {
                        fetched_choices.push(entry.word.toLowerCase());
                    }
                }
                if (fetched_choices.length < 3) {
                    fetch(
                        `/dictionary/api/${lang}/entries/?` +
                        `word!=${word}&` +
                        `num=${3 - fetched_choices.length}&`
                    )
                        .then(response => response.json())
                        .then(data => {
                            for (let entry of data) {
                                fetched_choices.push(entry.word.toLowerCase());
                            }
                            setChoices([...fetched_choices, matchWord].filter(Boolean).sort(() => Math.random() - 0.5));
                        })
                        .catch(error => {
                            if (error.response && error.response.status == 403) {
                                setMessage(["Too many retries. Try again later.", "warning"]);
                            }
                            console.error("Error fetching data: ", error);
                        });
                } else {
                    setChoices([...fetched_choices, matchWord].filter(Boolean).sort(() => Math.random() - 0.5));
                }
            })
            .catch(error => {
                if (error.respones && error.response.status == 403) {
                    setMessage(["Too many retries. Try again later.", "warning"]);
                }
                console.error("Error fetching data: ", error);
            });
    }, [matchWord]);

    React.useEffect(() => {
        matchWord && setChoices(prev => [...prev, matchWord.toLocaleLowerCase()].sort(() => Math.random() - 0.5));
    }, [matchWord]);

    React.useEffect(() => {
        choices.length === 4 && setChoicesReady(true);
    }, [choices])

    const handleChoiceClick = (choice) => {
        if (!answerSelected) {
            setSelectedChoice(choice);
            setIsCorrect(choice === matchWord);
            setAnswerSelected(true);
            setEndgame(true);
        }
    };

    return (
        <>
            {word && ( 
                <>
                    <Header title="Match" />
                    <div className="d-flex flex-column align-items-center text-center">
                        <div>
                            <h1 className="m-2 fs-3">Which is {mode} to <strong>{word}</strong>?</h1>
                        </div>
                        { message &&
                            <Message message={message[0]} variant={message[1]}/>
                        }
                        {endgame &&
                            <Message message={
                                <>{isCorrect ? "Correct." : "Incorrect."} The match of <a className="text-reset" href={`/dictionary/${lang}/entry/${word}`}>{word}</a> is <a className="text-reset" href={`/dictionary/${lang}/entry/${matchWord}`}>{matchWord}</a>.</>
                            }
                            variant={"info"}
                            />
                        }
                        { choicesReady ?
                            <Choices choices={choices} onClick={handleChoiceClick} selectedChoice={selectedChoice} matchWord={matchWord} answerSelected={answerSelected} />
                            : <Message message={"Generating choices..."} variant={"warning"}/>
                        }
                        {endgame ?
                            <Button onClick={() => {window.location.reload()}} variant="primary">Next</Button>
                            : <Button onClick={() => {window.location.reload()}} variant="secondary" disabled>Next</Button>
                        }
                    </div>
                </>
            )}
        </>
    )
}