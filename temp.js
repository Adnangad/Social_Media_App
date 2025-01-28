const url = "http://127.0.0.1:8000/signup/";
async function signup(ul) {
    const dat = {name: "Aboomi"}
    const response = await fetch(ul, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(dat)
        });
    if (response.status === 200) {
        console.log("Success");
    }
}
signup(url);