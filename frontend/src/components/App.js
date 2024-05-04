import React from 'react';
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Routes, Route, Link, Redirect } from "react-router-dom";
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

window.addEventListener("DOMContentLoaded", function (event) {
    ReactDOM.createRoot(
        document.querySelector("#app")
    )
    .render(
        <App />
    );
})