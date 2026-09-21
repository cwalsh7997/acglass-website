// Run: node .github/scripts/tests/test_gbp_attribution.js
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const script = fs.readFileSync(path.join(__dirname, '../../../js/acg-chrome.js'), 'utf8');
function run(search, storage = {}, action = 'https://formsubmit.co/connor@acglass.com', blocked = false) {
  const fields = {};
  const form = {
    getAttribute: () => action,
    querySelector: selector => fields[selector.match(/name="([^"]+)"/)[1]] || null,
    appendChild: input => { fields[input.name] = input; }
  };
  const document = {
    readyState: 'complete', querySelector: () => null,
    querySelectorAll: () => [form], createElement: () => ({})
  };
  const location = { pathname: '/send-plans.html', search };
  const sessionStorage = {
    getItem: key => { if (blocked) throw Error('blocked'); return storage[key]; },
    setItem: (key, value) => { if (blocked) throw Error('blocked'); storage[key] = value; },
    removeItem: key => { delete storage[key]; }
  };
  vm.runInNewContext(script, { document, location, URLSearchParams, window: { location, sessionStorage } });
  return Object.fromEntries(Object.entries(fields).map(([name, input]) => [name, input.value]));
}
const storage = {};
const query = '?utm_source=google&utm_medium=organic&utm_campaign=gbp_tampa&utm_content=website';
assert.deepEqual(run(query, storage), { utm_source: 'google', utm_medium: 'organic', utm_campaign: 'gbp_tampa', utm_content: 'website' });
assert.equal(run('', storage).utm_campaign, 'gbp_tampa', 'persists through internal navigation');
assert.deepEqual(run('?utm_source=newsletter', storage), {}, 'another campaign clears stale GBP attribution');
assert.deepEqual(run('', storage), {}, 'cleared campaign stays cleared');
assert.deepEqual(run(query, {}, '/search'), {}, 'does not affect other forms');
assert.equal(run(query, {}, undefined, true).utm_campaign, 'gbp_tampa', 'blocked storage does not break same-page submission');
assert.deepEqual(run('?utm_source=google&utm_medium=organic&utm_campaign=private@example.com'), {}, 'rejects arbitrary and potentially identifying campaign data');
assert.deepEqual(run('', { acg_gbp_attribution_v1: '{broken' }), {}, 'corrupt storage is harmless');
const all = ['west_palm_beach', 'stuart', 'tampa', 'naples'];
for (const city of all) assert.equal(run(query.replace('tampa', city)).utm_campaign, 'gbp_' + city);
console.log('GBP attribution: 11 checks passed. No network requests or lead submissions.');
