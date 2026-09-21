const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
test('only links into the MTM app emit open_mtm, without interfering with navigation',()=>{
  const events=[],handlers={};
  const context={URL,Date,window:{gtag:(...args)=>events.push(args)},location:{href:'https://serenityvalleyworks.com/morethanmeasured/',pathname:'/morethanmeasured/index.html'},document:{getElementById:()=>null,querySelector:()=>null,addEventListener:(n,fn)=>handlers[n]=fn}};
  vm.runInNewContext(fs.readFileSync(__dirname+'/../morethanmeasured/mtm.js','utf8'),context);
  const click=url=>handlers.click({target:{closest:()=>({href:url})}});
  click('https://randypoffinberger-design.github.io/Free-to-be-me/');
  click('https://example.com/');click('https://randypoffinberger-design.github.io/OtherApp/');
  assert.equal(events.length,1);assert.equal(events[0][1],'open_mtm');assert.equal(events[0][2].source_page,'/morethanmeasured/');
  context.window.gtag=undefined;assert.doesNotThrow(()=>click('https://randypoffinberger-design.github.io/Free-to-be-me/'));
});
