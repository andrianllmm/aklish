import React from "react";
import Header from "../Header";
import ProofreaderField from "./ProofreaderField";


export default function Proofreader() {
    return (
        <>
            <Header title="Proofreader" />
            <div className="container">
                <ProofreaderField defaultShowSuggestions={true} />
            </div>
        </>
    );
}
