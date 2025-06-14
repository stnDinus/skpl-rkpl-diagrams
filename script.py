import os
import re

# This script will parse a single text block containing multiple file
# definitions and create a .puml file for each one.

# The raw data containing all file definitions in the specified format.
puml_data = """
'=====================================================
' File: signup_activity.puml
'=====================================================
@startuml
|Pembeli|
start
:Mengisi form pendaftaran (email, password, dll);
|Sistem|
:Validasi data;
:Mengirim link konfirmasi ke email;
|Pembeli|
:Membuka email dan klik link konfirmasi;
|Sistem|
:Verifikasi token konfirmasi;
:Simpan data akun pembeli;
:Menampilkan notifikasi pendaftaran berhasil;
stop
@enduml

'=====================================================
' File: signup_seq.puml
'=====================================================
@startuml
actor Pembeli
boundary SignUpPage
entity Account

Pembeli -> SignUpPage : submit(data_pendaftaran)
activate SignUpPage
SignUpPage -> Account : create(data_pendaftaran)
activate Account
Account --> SignUpPage : success()
deactivate Account
SignUpPage --> Pembeli : Tampilkan halaman konfirmasi
deactivate SignUpPage
@enduml

'=====================================================
' File: signup_colab.puml
'=====================================================
@startuml
boundary SignUpPage
entity Account

(SignUpPage) -> (Account): create(data_pendaftaran)
@enduml

'=====================================================
' File: signin_activity.puml
'=====================================================
@startuml
|Pembeli|
start
:Masukkan email dan password;
|Sistem|
:Validasi kredensial;
if (Kredensial valid?) then (ya)
  :Buat sesi login;
  :Tampilkan halaman utama pembeli;
else (tidak)
  :Tampilkan pesan error;
endif
|Pembeli|
stop
@enduml

'=====================================================
' File: signin_seq.puml
'=====================================================
@startuml
actor Pembeli
boundary LoginPage
control Session

Pembeli -> LoginPage : submit(email, password)
activate LoginPage
LoginPage -> Session : create(email, password)
activate Session
Session --> LoginPage : loginSuccess()
deactivate Session
LoginPage --> Pembeli : Redirect ke halaman utama
deactivate LoginPage
@enduml

'=====================================================
' File: signin_colab.puml
'=====================================================
@startuml
boundary LoginPage
control Session

(LoginPage) -> (Session): create(email, password)
@enduml

'=====================================================
' File: signout_activity.puml
'=====================================================
@startuml
|Pembeli|
start
:Klik tombol keluar;
|Sistem|
:Hapus sesi login;
:Redirect ke halaman utama;
|Pembeli|
stop
@enduml

'=====================================================
' File: signout_seq.puml
'=====================================================
@startuml
actor Pembeli
boundary HomePage
control Session

Pembeli -> HomePage : logout()
activate HomePage
HomePage -> Session : destroy()
activate Session
Session --> HomePage : sessionDestroyed()
deactivate Session
HomePage --> Pembeli : Redirect ke halaman utama
deactivate HomePage
@enduml

'=====================================================
' File: signout_colab.puml
'=====================================================
@startuml
boundary HomePage
control Session

(HomePage) -> (Session): destroy()
@enduml

'=====================================================
' File: upload_design_activity.puml
'=====================================================
@startuml
|Pembeli|
start
:Pilih file desain;
:Klik tombol unggah;
|Sistem|
:Validasi file;
:Simpan file desain;
:Tampilkan notifikasi berhasil dan pratinjau;
|Pembeli|
stop
@enduml

'=====================================================
' File: upload_design_seq.puml
'=====================================================
@startuml
actor Pembeli
boundary UploadDesignPage
entity Design

Pembeli -> UploadDesignPage : upload(file)
activate UploadDesignPage
UploadDesignPage -> Design : create(fileData)
activate Design
Design --> UploadDesignPage : success(fileUrl)
deactivate Design
UploadDesignPage --> Pembeli : Tampilkan konfirmasi dan pratinjau
deactivate UploadDesignPage
@enduml

'=====================================================
' File: upload_design_colab.puml
'=====================================================
@startuml
boundary UploadDesignPage
entity Design

(UploadDesignPage) -> (Design): create(fileData)
@enduml

'=====================================================
' File: set_print_parameters_activity.puml
'=====================================================
@startuml
|Pembeli|
start
:Memilih desain yang sudah diunggah;
:Mengatur parameter (ukuran, bahan, jumlah);
:Simpan parameter;
|Sistem|
:Menyimpan konfigurasi parameter;
:Menampilkan hasil penyesuaian;
|Pembeli|
stop
@enduml

'=====================================================
' File: set_print_parameters_seq.puml
'=====================================================
@startuml
actor Pembeli
boundary PrintParametersPage
entity PrintConfig

Pembeli -> PrintParametersPage : setParameters(params)
activate PrintParametersPage
PrintParametersPage -> PrintConfig : save(params)
activate PrintConfig
PrintConfig --> PrintParametersPage : success()
deactivate PrintConfig
PrintParametersPage --> Pembeli : displayConfirmation()
deactivate PrintParametersPage
@enduml

'=====================================================
' File: set_print_parameters_colab.puml
'=====================================================
@startuml
boundary PrintParametersPage
entity PrintConfig

(PrintParametersPage) -> (PrintConfig): save(params)
@enduml

'=====================================================
' File: check_est_price_activity.puml
'=====================================================
@startuml
|Pembeli|
start
:Mengatur parameter cetak;
|Sistem|
:Menerima perubahan parameter;
:Menghitung estimasi harga berdasarkan parameter;
:Menampilkan estimasi harga;
|Pembeli|
stop
@enduml

'=====================================================
' File: check_est_price_seq.puml
'=====================================================
@startuml
actor Pembeli
boundary PrintParametersPage
control PriceEstimator

Pembeli -> PrintParametersPage : parametersChanged(params)
activate PrintParametersPage
PrintParametersPage -> PriceEstimator : calculate(params)
activate PriceEstimator
PriceEstimator --> PrintParametersPage : estimatedPrice
deactivate PriceEstimator
PrintParametersPage --> Pembeli : displayPrice(estimatedPrice)
deactivate PrintParametersPage
@enduml

'=====================================================
' File: check_est_price_colab.puml
'=====================================================
@startuml
boundary PrintParametersPage
control PriceEstimator

(PrintParametersPage) -> (PriceEstimator): calculate(params)
@enduml

'=====================================================
' File: acc_design_activity.puml
'=====================================================
@startuml
|Penjual|
start
:Melihat detail pesanan desain masuk;
:Pilih tindakan (Terima/Tolak/Revisi);
|Sistem|
:Update status pesanan desain;
:Kirim notifikasi ke pembeli;
|Penjual|
:Menerima konfirmasi update;
stop
@enduml

'=====================================================
' File: acc_design_seq.puml
'=====================================================
@startuml
actor Penjual
boundary AccDesignPage
entity DesignOrder
control Notification

Penjual -> AccDesignPage : submitAction(orderId, action)
activate AccDesignPage
AccDesignPage -> DesignOrder : updateStatus(action)
activate DesignOrder
DesignOrder -> Notification : sendToBuyer(status)
activate Notification
Notification --> DesignOrder : success()
deactivate Notification
DesignOrder --> AccDesignPage : statusUpdated()
deactivate DesignOrder
AccDesignPage --> Penjual : Tampilkan konfirmasi
deactivate AccDesignPage
@enduml

'=====================================================
' File: acc_design_colab.puml
'=====================================================
@startuml
boundary AccDesignPage
entity DesignOrder
control Notification

(AccDesignPage) -> (DesignOrder): updateStatus(action)
(DesignOrder) -> (Notification): sendToBuyer(status)
@enduml

'=====================================================
' File: transact_activity.puml
'=====================================================
@startuml
|Pembeli|
start
:Memeriksa rincian pesanan (harga, ongkir);
:Klik tombol 'Bayar';
:Memilih metode pembayaran;
:Melakukan transfer / pembayaran;
|Sistem|
:Redirect ke payment gateway;
:Menerima konfirmasi pembayaran;
:Update status pesanan menjadi 'Dibayar';
:Kirim notifikasi ke pembeli dan penjual;
|Pembeli|
:Menerima notifikasi pembayaran berhasil;
stop
@enduml

'=====================================================
' File: transact_seq.puml
'=====================================================
@startuml
actor Pembeli
boundary PaymentPage
control PaymentGateway
entity Order

Pembeli -> PaymentPage : pay()
activate PaymentPage
PaymentPage -> PaymentGateway : processPayment(details)
activate PaymentGateway
PaymentGateway -> Order : updatePaymentStatus(success)
activate Order
Order --> PaymentGateway : statusUpdated()
deactivate Order
PaymentGateway --> PaymentPage : paymentSuccess()
deactivate PaymentGateway
PaymentPage --> Pembeli : displaySuccessMessage()
deactivate PaymentPage
@enduml

'=====================================================
' File: transact_colab.puml
'=====================================================
@startuml
boundary PaymentPage
control PaymentGateway
entity Order

(PaymentPage) -> (PaymentGateway): processPayment(details)
(PaymentGateway) -> (Order): updatePaymentStatus(success)
@enduml

'=====================================================
' File: set_shipping_activity.puml
'=====================================================
@startuml
|Pembeli|
start
:Mengisi alamat pengiriman;
:Memilih jasa kurir;
|Sistem|
:Menghitung biaya ongkir berdasarkan alamat dan kurir;
:Menampilkan rincian biaya ongkir;
:Menambahkan ongkir ke total tagihan;
|Pembeli|
:Konfirmasi pilihan pengiriman;
stop
@enduml

'=====================================================
' File: set_shipping_seq.puml
'=====================================================
@startuml
actor Pembeli
boundary ShippingPage
control ShippingCostCalculator
entity Order

Pembeli -> ShippingPage : setShipping(address, courier)
activate ShippingPage
ShippingPage -> ShippingCostCalculator : calculate(address, courier)
activate ShippingCostCalculator
ShippingCostCalculator --> ShippingPage : shippingCost
deactivate ShippingCostCalculator
ShippingPage -> Order : addShippingCost(shippingCost)
activate Order
Order --> ShippingPage : success()
deactivate Order
ShippingPage --> Pembeli : displayTotal()
deactivate ShippingPage
@enduml

'=====================================================
' File: set_shipping_colab.puml
'=====================================================
@startuml
boundary ShippingPage
control ShippingCostCalculator
entity Order

(ShippingPage) -> (ShippingCostCalculator): calculate(address, courier)
(ShippingPage) -> (Order): addShippingCost(shippingCost)
@enduml

'=====================================================
' File: inspect_production_activity.puml
'=====================================================
@startuml
|Pembeli|
start
:Buka halaman riwayat pesanan;
:Pilih pesanan yang ingin dipantau;
|Sistem|
:Mengambil status produksi terakhir dari database;
:Menampilkan tahapan produksi (misal: 'desain diterima', 'pencetakan', 'pengemasan', 'dikirim');
|Pembeli|
stop
@enduml

'=====================================================
' File: inspect_production_seq.puml
'=====================================================
@startuml
actor Pembeli
boundary OrderDetailPage
entity Order

Pembeli -> OrderDetailPage : viewProductionStatus(orderId)
activate OrderDetailPage
OrderDetailPage -> Order : getProductionStatus()
activate Order
Order --> OrderDetailPage : currentStatus
deactivate Order
OrderDetailPage --> Pembeli : displayStatus(currentStatus)
deactivate OrderDetailPage
@enduml

'=====================================================
' File: inspect_production_colab.puml
'=====================================================
@startuml
boundary OrderDetailPage
entity Order

(OrderDetailPage) -> (Order): getProductionStatus()
@enduml

'=====================================================
' File: check_history_activity.puml
'=====================================================
@startuml
|Pembeli|
start
:Buka menu 'Riwayat Transaksi';
|Sistem|
:Mengambil semua data transaksi milik pembeli;
:Menampilkan daftar riwayat transaksi;
|Pembeli|
:Melihat daftar transaksi;
stop
@enduml

'=====================================================
' File: check_history_seq.puml
'=====================================================
@startuml
actor Pembeli
boundary HistoryPage
entity Order

Pembeli -> HistoryPage : viewHistory()
activate HistoryPage
HistoryPage -> Order : findAllByBuyer()
activate Order
Order --> HistoryPage : orderList
deactivate Order
HistoryPage --> Pembeli : displayHistory(orderList)
deactivate HistoryPage
@enduml

'=====================================================
' File: check_history_colab.puml
'=====================================================
@startuml
boundary HistoryPage
entity Order

(HistoryPage) -> (Order): findAllByBuyer()
@enduml
"""


def create_files_from_data():
    """
    Parses the puml_data string, extracts individual file definitions,
    and writes them to their respective .puml files.
    """
    # Get the directory where the script is located to save files there.
    try:
        # Assumes the script is being run from a file.
        output_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        # Fallback for interactive environments where __file__ is not defined.
        output_dir = os.getcwd()

    print(f"Files will be created in: {output_dir}\n")

    # This regex pattern finds all file definitions. It looks for the filename
    # in the header and then captures the entire @startuml...@enduml block.
    # re.DOTALL allows '.' to match newline characters.
    pattern = re.compile(
        r"' File: (.*?\.puml)"  # Group 1: Capture the filename ending in .puml
        r".*?"  # Non-greedily match the rest of the header
        r"(@startuml.*?@enduml)",  # Group 2: Capture the full content block
        re.DOTALL,
    )

    # Find all non-overlapping matches of the pattern in the string.
    matches = pattern.finditer(puml_data)

    files_created_count = 0
    total_files_found = 0

    for match in matches:
        total_files_found += 1
        filename = match.group(1).strip()
        content = match.group(2).strip()

        file_path = os.path.join(output_dir, filename)

        try:
            # Open the file in write mode with UTF-8 encoding and write content.
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Successfully created: {filename}")
            files_created_count += 1
        except IOError as e:
            # Print an error message if file creation fails.
            print(f"ERROR: Could not create file {filename}. Reason: {e}")

    # Final summary message.
    print(
        f"\nProcess finished. {files_created_count}/{total_files_found} files were created."
    )


# Run the main function when the script is executed.
if __name__ == "__main__":
    create_files_from_data()
