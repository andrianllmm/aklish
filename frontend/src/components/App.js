import React from 'react';
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Wordle from "./Games/Wordle/Wordle";
import Match from "./Games/Match/Match";
import Proofreader from "./Proofreader/Proofreader";


export default function App() {
    return (
        <Router>
            <Routes>
                <Route exact path="/games/wordle/:lang/" element={<Wordle />}></Route>
                <Route exact path="/games/match/:lang/" element={<Match />}></Route>
                <Route exact path="/proofreader/:lang/" element={<Proofreader />}></Route>
            </Routes>
        </Router>
    );
}

const appElement = document.querySelector("#app");
if (appElement) {
    window.addEventListener("DOMContentLoaded", () => {
        ReactDOM.createRoot(
            appElement
        )
        .render(
            <App />
        );
    })
}
