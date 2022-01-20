import { Controller } from "@hotwired/stimulus";

console.log("at least I'm in the file");

export default class extends Controller {
    static targets = ["submit"];

    connect() {
        console.log("CONNECTING Registration CONTROLLER....");
    }

    register() {
        console.log(this.element);
        // var searchResultsSection = document.querySelector("#searchResultsSection");
        // if (this.contentTarget.value.length < 1) {
        //     searchResultsSection.innerHTML = '';
        // }
        // console.log("trying to log content: ");
        // console.log(this.contentTarget);
        // console.log(this.contentTarget.value);
        console.log("roleTarget:");
        console.log(this.roleTarget);
        console.log("here is submitTarget:");
        console.log(this.submitTarget);
        this.submitTarget.click();
    }
}