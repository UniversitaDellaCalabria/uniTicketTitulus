document.addEventListener('DOMContentLoaded', function () {
    // --- LOGICA OP ---
    const addOpBtn = document.getElementById('add-op-row');
    const opContainer = document.getElementById('op-formset-container');
    const emptyOpTemplate = document.getElementById('empty-form-op-template').innerHTML;
    const opTotalForms = document.querySelector('input[name="op-TOTAL_FORMS"]');
    const opMaxFormsInput = document.querySelector('input[name="op-MAX_NUM_FORMS"]');
    const opMaxForms = opMaxFormsInput ? parseInt(opMaxFormsInput.value, 10) : 1000;

    function updateOpState() {
        if (!addOpBtn || !opContainer) return;
        const activeRows = opContainer.querySelectorAll('.op-form-row:not([style*="display: none"])').length;

        if (activeRows >= opMaxForms) {
            addOpBtn.style.display = 'none';
        } else {
            addOpBtn.style.display = '';
        }
    }

    addOpBtn.addEventListener('click', function () {
        const formCount = parseInt(opTotalForms.value);
        opContainer.insertAdjacentHTML('beforeend', emptyOpTemplate.replace(/__prefix__/g, formCount));
        opTotalForms.value = formCount + 1;
        updateOpState();
    });

    document.addEventListener('click', function (e) {
        const btn = e.target.closest('.remove-op-btn');
        if (btn) {
            const row = btn.closest('.op-form-row');
            const del = row.querySelector('input[type="checkbox"][name$="-DELETE"]');
            if (del) { del.checked = true; row.style.display = 'none'; } else { row.remove(); }
        }
        updateOpState();
    });

    // --- LOGICA CC ---
    const addCcBtn = document.getElementById('add-cc-row');
    const ccContainer = document.getElementById('cc-formset-container');
    const emptyCcTemplate = document.getElementById('empty-form-cc-template').innerHTML;
    const ccTotalForms = document.querySelector('input[name="cc-TOTAL_FORMS"]');
    const ccMaxFormsInput = document.querySelector('input[name="cc-MAX_NUM_FORMS"]');
    const ccMaxForms = ccMaxFormsInput ? parseInt(ccMaxFormsInput.value, 10) : 1000;

    function updateCcState() {
        if (!addCcBtn || !ccContainer) return;
        const activeRows = ccContainer.querySelectorAll('.cc-form-row:not([style*="display: none"])').length;

        if (activeRows >= ccMaxForms) {
            addCcBtn.style.display = 'none';
        } else {
            addCcBtn.style.display = '';
        }
    }

    addCcBtn.addEventListener('click', function () {
        const formCount = parseInt(ccTotalForms.value);
        ccContainer.insertAdjacentHTML('beforeend', emptyCcTemplate.replace(/__prefix__/g, formCount));
        ccTotalForms.value = formCount + 1;
        updateCcState();
    });

    document.addEventListener('click', function (e) {
        const btn = e.target.closest('.remove-cc-btn');
        if (btn) {
            const row = btn.closest('.cc-form-row');
            const del = row.querySelector('input[type="checkbox"][name$="-DELETE"]');
            if (del) { del.checked = true; row.style.display = 'none'; } else { row.remove(); }
        }
        updateCcState();
    });
    
    // Check iniziale sul numero massimo di form
    updateOpState();
    updateCcState();
});