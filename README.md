# PID - Social Media Platform

**PID.com** — bu zamonaviy qora fonli interfeysiga ega media kontent almashish va do‘stlar bilan muloqot qilish imkonini beradigan ijtimoiy tarmoq platformasi.  
Foydalanuvchilar **video blog** va **rasm shaklidagi postlar** joylashi, izohlashi va saqlab qo‘yishi mumkin.

---

## 📷 Ko‘rinishlari

| Profil Sahifasi | Postlar | Qidiruv Sahifasi |
| --------------- | ------- | ---------------- |
| ![Profile](READMEDM_Assets/Screenshot%202025-08-13%20at%201.30.20%20PM.png) | ![Posts](READMEDM_Assets/Screenshot%202025-08-13%20at%201.29.42%20PM.png) | ![Search](READMEDM_Assets/Screenshot%202025-08-13%20at%201.30.10%20PM.png) |

---

## ⭐ Asosiy Funksiyalar

- **Profil sahifasi** — foydalanuvchi haqida ma’lumot: avatar, bio va joylashtirilgan postlar  
- **Video postlar** — foydalanuvchilar video yuklashi va ko‘rishi mumkin  
- **Like va Saqlash** — yoqqan postlarga like bosish yoki keyinroq ko‘rish uchun saqlash imkoniyati  
- **Bloglar bo‘limi** — foydalanuvchilar o‘z maqolalarini yozib ulashishlari mumkin  
- **Qidiruv** — boshqa foydalanuvchilar va postlarni topish  
- **Do‘stlar bilan chat** — real vaqtli muloqot qilish imkoniyati  ( hali tayyor emas!)
- **Dark Mode UI** — zamonaviy va qulay interfeys  

---

## 🛠 Texnologiyalar

- **Frontend**: HTML, CSS (Dark Mode dizayn), JavaScript  
- **Backend**: Python (Django)
- **Ma’lumotlar bazasi**: PostgreSQL
- **Video Player**: HTML5 video player integratsiyasi  

---

## 🚀 O‘rnatish

1. Loyihani klon qiling:
   ```bash
   git clone https://github.com/ABDULHODIY1/Media-with-django.git
   cd Media-with-django
   ```

## ⚙️ Muhit o‘zgaruvchilari (environment variables)

Lokal ishlab chiqishda hech narsa sozlash shart emas — standart qiymatlar avvalgidek ishlaydi.
Serverga (production) chiqarishda quyidagilarni o‘rnating:

| O‘zgaruvchi | Standart qiymat | Izoh |
|---|---|---|
| `DJANGO_DEBUG` | `true` | Production'da `false` qiling |
| `DJANGO_SECRET_KEY` | (faqat DEBUG'da ishlaydigan dev kalit) | `DJANGO_DEBUG=false` bo‘lsa majburiy |
| `DJANGO_ALLOWED_HOSTS` | DEBUG'da `*`, aks holda `localhost,127.0.0.1` | Vergul bilan: `example.com,www.example.com` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | bo‘sh | Masalan: `https://example.com` |
| `POSTGRES_DB` / `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_HOST` / `POSTGRES_PORT` | `mydatabase` / `thony123` / `mypassword` / `127.0.0.1` / `5432` | PostgreSQL ulanishi |

Yangi maxfiy kalit yaratish:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Muhit sozlamalari testlarini PostgreSQL serveriga ulanmasdan ishga tushirish:
```bash
python -m pip install Django==5.2.4
python -m unittest discover -s tests -v
```
