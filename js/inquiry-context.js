(function () {
  const params = new URLSearchParams(window.location.search);
  const product = (params.get('product') || '').trim().slice(0, 80);
  const project = (params.get('project') || '').trim().slice(0, 120);
  if (!product && !project) return;

  const subject = document.getElementById('contact-subject');
  const message = document.getElementById('contact-message');
  if (!subject || !message || subject.value || message.value) return;

  const lang = document.documentElement.lang;
  const labels = lang === 'zh-TW'
    ? { productSubject: '產品詢價：', productMessage: '我想詢問此產品的商用專案資訊：', projectSubject: '類似案例專案諮詢：', projectMessage: '我想討論與此案例相似的家具專案：' }
    : lang === 'ja'
      ? { productSubject: '製品見積もり：', productMessage: 'この製品について、商業プロジェクト向けの情報を希望します：', projectSubject: '類似プロジェクトのご相談：', projectMessage: 'この導入事例に類似する家具プロジェクトについて相談を希望します：' }
      : { productSubject: 'Product enquiry: ', productMessage: 'I would like commercial project information for this product: ', projectSubject: 'Similar project enquiry: ', projectMessage: 'I would like to discuss a furniture project similar to this case: ' };

  const projectNames = {
    'kai-restaurant-furniture-installation': { en: 'Kai Restaurant Furniture Installation', 'zh-TW': 'Kai 餐廳家具安裝紀錄', ja: 'Kai レストラン家具導入記録' },
    'legoland-cafeteria-furniture-installation': { en: 'Legoland Cafeteria Furniture Installation', 'zh-TW': 'Legoland 餐廳家具安裝紀錄', ja: 'LEGOLAND カフェテリア家具導入記録' },
    'll-waterpark-poolside-furniture-installation': { en: 'LL Waterpark Poolside Furniture Installation', 'zh-TW': 'LL 水上樂園池畔家具安裝紀錄', ja: 'LL ウォーターパーク・プールサイド家具導入記録' }
  };

  if (product) {
    subject.value = labels.productSubject + product;
    message.value = labels.productMessage + product + '\n\n';
  } else {
    const readableProject = projectNames[project]?.[lang] || project.replace(/-/g, ' ');
    subject.value = labels.projectSubject + readableProject;
    message.value = labels.projectMessage + readableProject + '\n\n';
  }
})();
