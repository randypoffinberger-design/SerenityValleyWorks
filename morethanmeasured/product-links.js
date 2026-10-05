(() => {
  const input=document.getElementById('product-search');
  const items=[...document.querySelectorAll('[data-product-id]')];
  const total=new Set(items.map(item=>item.dataset.productId)).size;
  input.addEventListener('input',()=>{
    const query=input.value.trim().toLocaleLowerCase();
    const matching=new Set();
    for(const item of items){item.hidden=!item.textContent.toLocaleLowerCase().includes(query);if(!item.hidden)matching.add(item.dataset.productId);}
    for(const section of document.querySelectorAll('.directory-subgroup')){
      const count=section.querySelectorAll('li:not([hidden])').length;
      section.hidden=count===0;
      section.querySelector('.subcategory-count').textContent=`(${count})`;
    }
    for(const section of document.querySelectorAll('.directory-section')){
      const count=section.querySelectorAll('li:not([hidden])').length;
      section.hidden=count===0;
      section.querySelector('.category-count').textContent=`(${count})`;
    }
    document.getElementById('product-count').textContent=`Showing ${matching.size} of ${total} products.`;
    document.getElementById('product-empty').hidden=matching.size!==0;
  });
})();
