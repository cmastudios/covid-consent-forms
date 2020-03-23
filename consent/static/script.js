function disable()
{
    document.getElementById('id_inability_reason').value = "";
    document.getElementById('id_representative_name').value = "";
    document.getElementById('id_relationship_to_patient').value = "";

    document.getElementById('unable_to_consent_section').style.display = "none";
}
function enable()
{
    document.getElementById('unable_to_consent_section').style.display = "inherit";
}

window.addEventListener('load', (event) =>
{
    document.getElementById("id_ability_to_consent").addEventListener('change', () =>
    {
        if (document.getElementById('id_ability_to_consent').value == 1)
        {
            disable();
        }
        else
        {
            enable();
        }
    });
});