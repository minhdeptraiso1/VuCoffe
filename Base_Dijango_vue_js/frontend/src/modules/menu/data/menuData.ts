export interface MenuItem {
  id: string;
  name: string;
  category: "signature" | "traditional" | "modern" | "coldbrew" | "tea" | "pastry";
  price: number;
  formattedPrice: string;
  tag: string;
  isBestSeller?: boolean;
  isNew?: boolean;
  description: string;
  image: string;
  illustrationType:
    | "salted-coffee"
    | "egg-coffee"
    | "bac-xiu"
    | "cold-brew"
    | "black-coffee"
    | "milk-coffee"
    | "latte"
    | "cappuccino"
    | "matcha"
    | "fruit-tea"
    | "peach-tea"
    | "croissant"
    | "tiramisu"
    | "cheesecake";
  volume?: string;
  calories?: number;
  roastLevel?: string;
  ingredients: string[];
  rating: number;
  reviewCount: number;
}

export interface CategoryOption {
  id: string;
  label: string;
  icon: string;
  iconName: string;
}

export const MENU_CATEGORIES: CategoryOption[] = [
  { id: "all", label: "Tất cả món", icon: "☕", iconName: "Coffee" },
  { id: "traditional", label: "Cà phê truyền thống", icon: "🇻🇳", iconName: "Flame" },
  { id: "modern", label: "Espresso & Latte", icon: "✨", iconName: "CupSoda" },
  { id: "coldbrew", label: "Cold Brew ủ lạnh", icon: "🧊", iconName: "GlassWater" },
  { id: "tea", label: "Trà & Giải nhiệt", icon: "🍃", iconName: "Leaf" },
  { id: "pastry", label: "Bánh ngọt điểm tâm", icon: "🥐", iconName: "Cake" },
];

export const MENU_ITEMS: MenuItem[] = [
  // 1. Signature
  {
    id: "kt-01",
    name: "Cà phê Muối Kim Thành",
    category: "signature",
    price: 35000,
    formattedPrice: "35.000 đ",
    tag: "Đặc sản bán chạy",
    isBestSeller: true,
    description:
      "Cốt Robusta Đắk Lắk đậm đặc hòa quyện cùng lớp kem muối biển béo ngậy mềm mịn, tạo nên vị đắng ngọt mặn hài hòa khó quên.",
    image:
      "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=800&q=80",
    illustrationType: "salted-coffee",
    volume: "350ml",
    calories: 185,
    roastLevel: "Đậm vừa (Medium Dark)",
    ingredients: ["Robusta Đắk Lắk", "Kem muối biển tươi", "Sữa đặc", "Đá viên"],
    rating: 4.9,
    reviewCount: 342,
  },
  {
    id: "kt-02",
    name: "Cà phê Trứng Hanoian",
    category: "signature",
    price: 42000,
    formattedPrice: "42.000 đ",
    tag: "Trứ danh Hà Thành",
    isBestSeller: true,
    description:
      "Lớp kem trứng gà tươi đánh bông sánh mịn như nhung, giữ nóng lâu trên nền cà phê phin nguyên chất đắng thơm nồng nàn.",
    image:
      "https://images.unsplash.com/photo-1541167760496-1628856ab772?auto=format&fit=crop&w=800&q=80",
    illustrationType: "egg-coffee",
    volume: "280ml",
    calories: 220,
    roastLevel: "Đậm (Dark Roast)",
    ingredients: ["Lòng đỏ trứng gà tươi", "Cà phê phin Robusta", "Mật ong hoa rừng", "Sữa đặc"],
    rating: 4.9,
    reviewCount: 285,
  },

  // 2. Traditional
  {
    id: "kt-03",
    name: "Bạc Xỉu Cốt Dừa 3 Tầng",
    category: "traditional",
    price: 38000,
    formattedPrice: "38.000 đ",
    tag: "Yêu thích nhất",
    isBestSeller: true,
    description:
      "Sự hòa quyện 3 tầng đẹp mắt giữa sữa đặc ngọt dịu, nước cốt dừa Bến Tre béo bùi và cà phê phin đậm đà thơm ngát.",
    image:
      "https://images.unsplash.com/photo-1572442388796-11668ba67e53?auto=format&fit=crop&w=800&q=80",
    illustrationType: "bac-xiu",
    volume: "400ml",
    calories: 245,
    roastLevel: "Đậm vừa",
    ingredients: ["Cà phê phin", "Nước cốt dừa Bến Tre", "Sữa đặc", "Sữa tươi"],
    rating: 4.8,
    reviewCount: 198,
  },
  {
    id: "kt-04",
    name: "Cà Phê Sữa Đá Sài Gòn",
    category: "traditional",
    price: 32000,
    formattedPrice: "32.000 đ",
    tag: "Kinh điển",
    isBestSeller: true,
    description:
      "Cà phê Robusta mộc pha phin nhỏ giọt truyền thống, kết hợp sữa đặc Ông Thọ sánh ngọt và đá lạnh mát rượi.",
    image:
      "https://images.unsplash.com/photo-1517256064527-09c73fc73e38?auto=format&fit=crop&w=800&q=80",
    illustrationType: "milk-coffee",
    volume: "350ml",
    calories: 160,
    roastLevel: "Đậm truyền thống",
    ingredients: ["100% Robusta Tây Nguyên", "Sữa đặc cao cấp", "Đá viên sạch"],
    rating: 4.8,
    reviewCount: 420,
  },
  {
    id: "kt-05",
    name: "Cà Phê Đen Phin Đậm Vị",
    category: "traditional",
    price: 29000,
    formattedPrice: "29.000 đ",
    tag: "Chuẩn gu Việt",
    description:
      "100% Robusta hạt mộc rang mộc mẻ nhỏ, vị đắng đậm đà, hương thơm chocolate tự nhiên và hậu vị ngọt sâu lắng dài lâu.",
    image:
      "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=800&q=80",
    illustrationType: "black-coffee",
    volume: "300ml",
    calories: 15,
    roastLevel: "Đậm (Dark Roast)",
    ingredients: ["Hạt Robusta mộc sàng 18", "Đường mía nâu (tùy chọn)"],
    rating: 4.9,
    reviewCount: 165,
  },

  // 3. Modern & Espresso
  {
    id: "kt-06",
    name: "Caramel Macchiato Hạt Dẻ",
    category: "modern",
    price: 46000,
    formattedPrice: "46.000 đ",
    tag: "Ngọt ngào",
    isNew: true,
    description:
      "Espresso kép chiết xuất từ Arabica Cầu Đất hòa cùng sữa tươi thanh trùng đánh nóng và sốt caramel vani béo ngậy.",
    image:
      "https://images.unsplash.com/photo-1485808191679-5f86510681a2?auto=format&fit=crop&w=800&q=80",
    illustrationType: "latte",
    volume: "380ml",
    calories: 210,
    roastLevel: "Trung bình (Medium Roast)",
    ingredients: ["Double Shot Espresso", "Sữa tươi thanh trùng", "Sốt Caramel Pháp", "Vani"],
    rating: 4.8,
    reviewCount: 92,
  },
  {
    id: "kt-07",
    name: "Cappuccino Bột Quế Thơm",
    category: "modern",
    price: 42000,
    formattedPrice: "42.000 đ",
    tag: "Ý ấm cúng",
    description:
      "Tỷ lệ hoàn hảo 1:1:1 giữa espresso đậm đà, sữa nóng và bọt sữa bông dày xốp, rắc bột quế Trà Bồng thơm lừng.",
    image:
      "https://images.unsplash.com/photo-1534778101976-62847782c213?auto=format&fit=crop&w=800&q=80",
    illustrationType: "cappuccino",
    volume: "300ml",
    calories: 140,
    roastLevel: "Trung bình",
    ingredients: ["Espresso Arabica", "Bọt sữa mịn micro-foam", "Bột quế tự nhiên"],
    rating: 4.7,
    reviewCount: 88,
  },

  // 4. Cold Brew
  {
    id: "kt-08",
    name: "Cold Brew Cam Quế Thảo Mộc",
    category: "coldbrew",
    price: 45000,
    formattedPrice: "45.000 đ",
    tag: "Thanh mát",
    isBestSeller: true,
    description:
      "Cà phê Arabica Cầu Đất ủ lạnh 18 tiếng, chiết xuất vị chua thanh tự nhiên cùng hương thơm mát từ lát cam vàng và thanh quế.",
    image:
      "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?auto=format&fit=crop&w=800&q=80",
    illustrationType: "cold-brew",
    volume: "420ml",
    calories: 65,
    roastLevel: "Sáng vừa (Light Medium)",
    ingredients: ["Arabica ủ lạnh 18h", "Cam vàng Úc tươi", "Quế thanh", "Mật ong tự nhiên"],
    rating: 4.9,
    reviewCount: 214,
  },
  {
    id: "kt-09",
    name: "Cold Brew Chanh Vàng Mật Ong",
    category: "coldbrew",
    price: 45000,
    formattedPrice: "45.000 đ",
    tag: "Giải tỏa mệt mỏi",
    description:
      "Vị chua dịu nhẹ sảng khoái của chanh vàng kết hợp mật ong rừng nguyên chất trên nền cà phê ủ lạnh thanh thoát.",
    image:
      "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=800&q=80",
    illustrationType: "cold-brew",
    volume: "420ml",
    calories: 75,
    roastLevel: "Sáng vừa",
    ingredients: ["Arabica Cold Brew", "Chanh vàng lát", "Mật ong hoa nhãn", "Lá bạc hà"],
    rating: 4.8,
    reviewCount: 110,
  },

  // 5. Tea & Refreshment
  {
    id: "kt-10",
    name: "Trà Oolong Đào Dâu Tằm",
    category: "tea",
    price: 39000,
    formattedPrice: "39.000 đ",
    tag: "Giải nhiệt ngày hè",
    isBestSeller: true,
    description:
      "Lá trà Oolong Bảo Lộc đậm vị chát nhẹ ngọt hậu, kết hợp miếng đào giòn tươi và mứt dâu tằm Đà Lạt tự nấu thơm lừng.",
    image:
      "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=800&q=80",
    illustrationType: "peach-tea",
    volume: "500ml",
    calories: 120,
    ingredients: ["Cốt trà Oolong Bảo Lộc", "Đào ngâm giòn", "Mứt dâu tằm tươi", "Chanh tươi"],
    rating: 4.8,
    reviewCount: 176,
  },
  {
    id: "kt-11",
    name: "Trà Mãng Cầu Xiêm Tươi",
    category: "tea",
    price: 42000,
    formattedPrice: "42.000 đ",
    tag: "Hot trend",
    isNew: true,
    description:
      "Thịt mãng cầu tươi dầm ngọt thanh chua dịu, hòa cùng trà lài ướp hoa tươi thanh khiết, giải nhiệt tức thì.",
    image:
      "https://images.unsplash.com/photo-1497534446932-c925b458314e?auto=format&fit=crop&w=800&q=80",
    illustrationType: "fruit-tea",
    volume: "500ml",
    calories: 135,
    ingredients: ["Trà lài tươi", "Thịt mãng cầu xiêm", "Đường phèn", "Hạt chia"],
    rating: 4.9,
    reviewCount: 145,
  },
  {
    id: "kt-12",
    name: "Matcha Latte Kem Phô Mai",
    category: "tea",
    price: 45000,
    formattedPrice: "45.000 đ",
    tag: "Mịn mượt",
    description:
      "Bột matcha Uji Nhật Bản nguyên chất khuấy đều cùng sữa tươi béo thơm, phủ lớp kem cheese mằn mặn mịn màng.",
    image:
      "https://images.unsplash.com/photo-1536256263959-770b48d82b0a?auto=format&fit=crop&w=800&q=80",
    illustrationType: "matcha",
    volume: "400ml",
    calories: 230,
    ingredients: ["Bột Matcha Uji Nhật", "Sữa tươi Dalat Milk", "Kem phô mai tươi", "Đá viên"],
    rating: 4.8,
    reviewCount: 130,
  },

  // 6. Pastry
  {
    id: "kt-13",
    name: "Croissant Bơ Pháp Nướng Giòn",
    category: "pastry",
    price: 32000,
    formattedPrice: "32.000 đ",
    tag: "Nướng nóng mỗi sáng",
    isBestSeller: true,
    description:
      "Bánh sừng bò nghìn lớp thơm nức mùi bơ nhập khẩu Pháp, vỏ ngoài giòn rụm, bên trong xốp mềm béo ngậy.",
    image:
      "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=800&q=80",
    illustrationType: "croissant",
    calories: 260,
    ingredients: ["Bột mì cao cấp", "Bơ Pháp Elle & Vire", "Men tự nhiên", "Trứng"],
    rating: 4.9,
    reviewCount: 195,
  },
  {
    id: "kt-14",
    name: "Bánh Tiramisu Cà Phê Espresso",
    category: "pastry",
    price: 45000,
    formattedPrice: "45.000 đ",
    tag: "Đặc biệt",
    description:
      "Lớp bánh ladyfinger thấm đẫm cà phê espresso đậm đà của quán, xen kẽ kem Mascarpone béo thơm và bột cacao Bỉ.",
    image:
      "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?auto=format&fit=crop&w=800&q=80",
    illustrationType: "tiramisu",
    calories: 310,
    ingredients: ["Phô mai Mascarpone", "Cà phê Espresso Kim Thành", "Bánh Savoiardi", "Cacao Bỉ"],
    rating: 4.9,
    reviewCount: 160,
  },
  {
    id: "kt-15",
    name: "Bánh Mousse Chanh Leo",
    category: "pastry",
    price: 38000,
    formattedPrice: "38.000 đ",
    tag: "Thanh mát chua ngọt",
    isNew: true,
    description:
      "Lớp mousse chanh leo chua ngọt dịu nhẹ tan ngay đầu lưỡi, phủ mặt thạch bóng bẩy thơm nồng nàn vị trái cây nhiệt đới.",
    image:
      "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&w=800&q=80",
    illustrationType: "cheesecake",
    calories: 220,
    ingredients: ["Nước cốt chanh leo tươi", "Kem tươi Whipping", "Bông lan vani", "Gelatin"],
    rating: 4.7,
    reviewCount: 78,
  },
];
