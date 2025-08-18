$(document).ready(function () {
  fetch("drivers.json")
    .then(response => response.json())
    .then(data => {
      let rows = data.map(d => [
        d.cust_id,
        d.name,
        d.formula.irating,
        d.formula.sr,
        d.formula.license,
        d.sportscar.irating,
        d.sportscar.sr,
        d.sportscar.license
      ]);

      $('#drivers').DataTable({
        data: rows,
        columns: [
          { title: "iRacing ID" },
          { title: "Navn" },
          { title: "iRating Formel" },
          { title: "SR Formel" },
          { title: "Licens Formel" },
          { title: "iRating Sportscar" },
          { title: "SR Sportscar" },
          { title: "Licens Sportscar" }
        ],
        pageLength: 25
      });
    });
});
