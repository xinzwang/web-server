var cur = "0";

function goto(page)
{
    if(page !== cur)
    {
        var navcur = document.getElementById("nav" + page);
        navcur.style.borderBottom = "2px solid #3e315d";
        var navpre = document.getElementById("nav" + cur);
        navpre.style.borderBottom = "none";
        console.log(navcur);

        var pre = document.getElementById(cur);
        var now = document.getElementById(page);

        if(parseInt(page) < parseInt(cur))
        {

        }

        pre.style.display = "none";
        now.style.display = "flex";

        cur = page;
    }
}