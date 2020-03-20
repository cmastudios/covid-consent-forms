function disable()
{
    document.getElementById('id_inability_reason').disabled = true;
    document.getElementById('id_representative_name').disabled = true;
    document.getElementById('id_relationship_to_patient').disabled = true;
    document.getElementById('id_inability_reason').value = "";
    document.getElementById('id_representative_name').value = "";
    document.getElementById('id_relationship_to_patient').value = "";
}
function enable()
{
    document.getElementById('id_inability_reason').disabled = false;
    document.getElementById('id_representative_name').disabled = false;
    document.getElementById('id_relationship_to_patient').disabled = false;
}

window.addEventListener('load', (event) =>
{
    disable();
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