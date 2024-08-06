import React from "react";
import Header from "../Header";
import ProofreaderField from "./ProofreaderField";


export default function Proofreader() {
    return (
        <>
            <Header title="Proofreader" />
            <ProofreaderField defaultShowSuggestions={true} />
        </>
    );
}
