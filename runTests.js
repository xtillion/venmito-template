import { exec } from "child_process";

exec("python3 tests/*.py", (error, stdout, stderr) => {
    if (error) {
        console.error(` Error executing Python tests: ${error.message}`);
        return;
    }
    if (stderr) {
        console.error(`Python script error: ${stderr}`);
        return;
    }
    console.log(`Python tests output:\n${stdout}`);
});
