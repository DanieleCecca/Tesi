function delete_exercise(exercise_id) {
    fetch("/delete-exercise", {
      method: "POST",
      body: JSON.stringify({ exercise_id: exercise_id }),
    }).then((_res) => {
      window.location.href = "/create-routine";
    });
  }