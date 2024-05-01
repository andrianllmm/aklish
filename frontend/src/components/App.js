import React from 'react';
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Routes, Route, Link, Redirect } from "react-router-dom";
import Wordle from "./Games/Wordle/Wordle"


export default function App() {
    return (
        <Router>
            <Routes>
                <Route exact path="/games/wordle/" element={<Wordle />}></Route>
            </Routes>
        </Router>
    );
}

window.addEventListener("DOMContentLoaded", function (e) {
    ReactDOM.createRoot(
        document.querySelector("#app")
    )
    .render(
        <App />
    );
})