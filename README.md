# **Animal Classification using TensorFlow Lite** 🐱🐶🐘🐴🦁

## **Setup Environment - Anaconda**
Untuk menjalankan proyek ini, Anda dapat membuat environment baru menggunakan Anaconda. Hal ini akan memastikan bahwa semua dependensi yang diperlukan terinstal dengan baik.

## **Setup Environment - Shell/Terminal**
Jika Anda lebih memilih menggunakan venv, Anda dapat membuat environment virtual menggunakan `python -m venv` di terminal atau shell Anda. Pastikan untuk mengaktifkan environment ini dan menginstal dependensi yang diperlukan.

## **Data Preprocessing and Augmentation**
Proyek ini menggunakan dataset klasifikasi gambar hewan yang terdiri dari sekitar 15.000 gambar dari lima kelas: kucing, anjing, gajah, kuda, dan singa. Dataset ini diambil dari Google Images dan telah dibersihkan untuk menghilangkan gambar yang tidak relevan.

Data dibagi menjadi tiga bagian utama: data pelatihan (training), data pengujian (test), dan data validasi (validation). Pembagian ini dilakukan untuk memastikan bahwa model dapat diuji dengan data yang tidak digunakan selama pelatihan, sehingga dapat mengukur generalisasi model.

Untuk meningkatkan keberagaman data pelatihan dan membantu model belajar lebih baik, dilakukan augmentasi data. Augmentasi data meliputi rotasi gambar, pergeseran horizontal dan vertikal, zooming, serta flipping. Teknik ini bertujuan untuk meningkatkan variasi data sehingga model dapat lebih robust terhadap perubahan kecil pada gambar yang diinputkan.

## **Model Architecture**
Model yang digunakan dalam proyek ini adalah Convolutional Neural Network (CNN), yang sangat efektif dalam menangani tugas klasifikasi gambar. Model ini memiliki beberapa lapisan konvolusi dan pooling untuk mengekstraksi fitur dari gambar, diikuti dengan lapisan dense untuk melakukan klasifikasi akhir.

Model ini dilatih menggunakan data pelatihan yang telah diaugmentasi, dan dievaluasi dengan menggunakan data validasi yang telah disiapkan sebelumnya. Proses pelatihan dilakukan dengan optimisasi Adam dan menggunakan fungsi loss `categorical_crossentropy` karena ini adalah masalah klasifikasi multikelas.

## **Model Conversion to TensorFlow Lite**
Setelah model dilatih, model dapat dikonversi menjadi format TensorFlow Lite. Format ini memungkinkan model dijalankan pada perangkat dengan sumber daya terbatas, seperti ponsel atau perangkat embedded. Konversi ini sangat penting untuk aplikasi yang membutuhkan inferensi model di perangkat yang tidak memiliki GPU atau perangkat keras canggih lainnya.

## **Run Inference with TensorFlow Lite**
Setelah model berhasil dikonversi menjadi format TensorFlow Lite, model dapat digunakan untuk inferensi pada gambar baru. Proses ini dilakukan dengan memuat model TensorFlow Lite, menyiapkan input gambar, dan menjalankan inferensi untuk mendapatkan prediksi kelas dari gambar yang dimasukkan.

## **Fitur Model**
- **Klasifikasi Gambar Hewan:** Model dapat mengklasifikasikan gambar ke dalam lima kelas: Kucing, Anjing, Gajah, Kuda, dan Singa. Setiap gambar yang dimasukkan ke dalam model akan diprediksi berdasarkan kelas yang paling sesuai.
- **Augmentasi Data:** Augmentasi data digunakan untuk meningkatkan kualitas model dengan menambahkan variasi pada data pelatihan, yang akan membantu model mengenali objek dalam berbagai kondisi.
- **TensorFlow Lite:** Setelah pelatihan, model dapat dikonversi menjadi format TensorFlow Lite yang dapat dijalankan pada perangkat dengan sumber daya terbatas seperti ponsel.

## **Catatan**
- Gambar yang dimasukkan untuk inferensi harus memiliki ukuran yang sesuai dengan ukuran input yang diharapkan oleh model (150x150x3).
- Proses pelatihan memerlukan dataset yang sudah dibagi menjadi data pelatihan, pengujian, dan validasi untuk menghindari overfitting dan memastikan model memiliki kemampuan generalisasi yang baik.

