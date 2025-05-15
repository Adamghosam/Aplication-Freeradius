
from flask import Flask, render_template, request, flash,url_for,redirect
from flask_mysqldb import MySQL
import random
import datetime

app = Flask(__name__,static_folder='static')

# Set the secret key
app.secret_key = 'Sapiasia'

# MySQL configuration
app.config['MYSQL_HOST'] = '172.16.0.206'
app.config['MYSQL_USER'] = 'Alisa'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'radius'

mysql = MySQL(app)


# start home
@app.route('/')
def home():
    return render_template('index.html')



@app.route('/tambahbaru')
def tambah():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM userclient")
    data = cur.fetchall()
    cur.close()
    return render_template('dataclient.html',userclient=data)


# end home



# start tabel client
@app.route('/client')
def client():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM radcheck")
    data = cur.fetchall()
    cur.close()
    return render_template('client.html', radcheck=data)
# end tabel client


# start genret vocer
@app.route('/generate', methods=['GET','POST'])
def generate_code():
 
    attribute = 'Cleartext-Password'
    op = ':='
    code_length = 5
    quantity = int(request.form['quantity'])


   

        # return redirect(url_for('home'))
    codes = []

    try:
        # Create a cursor to interact with the database
        cur = mysql.connection.cursor()

        for _ in range(quantity):
            code = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=code_length))
            codes.append(code)

            for _ in range(quantity):
                sapi = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=code_length))
                codes.append(sapi)

            # Execute the INSERT statement
            cur.execute("INSERT INTO radcheck (username, attribute, op, value) VALUES (%s, %s, %s, %s)",
                        (sapi, attribute, op, code))

        # Commit the transaction
        mysql.connection.commit()
        cur.close()
        # Close the cursor

      
        # if request.method == 'POST':
        #     name = request.form['quantity']
        flash("Data : {} Berhasil Ditambahkan " .format(quantity), "success")
        return redirect(url_for('home'))
    except Exception as e:
        flash("Terjadi kesalahan saat memproses permintaan", "error")
        return redirect(url_for('home'))

            

        
       
        

    #     # return render_template('client.html', codes=codes)
    #     return redirect(url_for('home'))
    # except Exception as e:
    #     return f"Error: {str(e)}"

# End genret vocer


# @app.route('/generate_unique_number', methods=['POST'])
# def generate_unique_number():
#     if request.method == 'POST':
#         Nama = request.form['nama']
#         Notelp = request.form['notelp']
#         Alamat = request.form['alamat']
#         current_date = datetime.datetime.now()
#         year = current_date.year
#         month = current_date.month
        

#         try:
#             # Read nomor urut from the database
#             cur = mysql.connection.cursor()
#             cur.execute("SELECT nourut FROM nomerurut")
#             result = cur.fetchone()

#             if result:
#                 nourut = result[0]
#             else:
#                 nourut = 1

#             # Format nomor urut with 3 digits
#             nomor_urut_formatted = int(nourut).zfill(3)

#             # Increase nomor urut for next usage
#             nourut += 1

#             # Update nomor urut in the database
#             cur.execute("UPDATE nomerurut SET nourut = %s", (nourut,))
#             mysql.connection.commit()

#             # Combine year, month, and nomor urut
#             unique_number = f"{year}{month:02d-}{nomor_urut_formatted}"

#             # Insert client data into the database
#             cur.execute("INSERT INTO userclient (noregis, nama, alamat, notelpon) VALUES (%s, %s, %s, %s)",
#                         (unique_number, Nama, Alamat, Notelp))
#             mysql.connection.commit()
#             cur.close()

#             flash("User : {} Berhasil Ditambahkan " .format(Nama), "success")
#             return redirect(url_for('tambah'))
#         except Exception as e:
#             flash("Terjadi kesalahan saat memproses permintaan", "error")
#             return redirect(url_for('tambah'))

#     # return render_template('tambah.html')

# # isert data client
@app.route('/generate_unique_number', methods=['POST'])
def generate_unique_number():
    if request.method == 'POST':
        Nama = request.form['nama']
        Notelp = request.form['notelp']
        Alamat = request.form['alamat']
        current_date = datetime.datetime.now()
        year = current_date.year
        month = current_date.month

        try:
            # Read nomor urut from the database
            cur = mysql.connection.cursor()
            cur.execute("SELECT nourut FROM nomerurut")
            result = cur.fetchone()

            if result:
                nourut = result[0]
            else:
                nourut = 1

            # Format nomor urut with 3 digits
            nomor_urut_formatted = str(nourut).zfill(3)

            # Increase nomor urut for next usage
            nourut += 1

            # Update nomor urut in the database
            cur.execute("UPDATE nomerurut SET nourut = %s", (nourut,))
            mysql.connection.commit()

            # Combine year, month, and nomor urut
            unique_number = f"{year}{month:02d}{nomor_urut_formatted}"

            # Insert client data into the database
            cur.execute("INSERT INTO userclient (noregis, nama, alamat, notelpon) VALUES (%s, %s, %s, %s)",
                        (unique_number, Nama, Alamat, Notelp))
            mysql.connection.commit()
            cur.close()

            flash("User: {} Berhasil Ditambahkan".format(Nama), "success")
            return redirect(url_for('tambah'))
        except Exception as e:
            flash("Terjadi kesalahan saat memproses permintaan", "error")
            return redirect(url_for('tambah'))




@app.route('/delete', methods=['POST'])
def delete_data():
    try:
        data_id = request.form.get('id')
        cur = mysql.connection.cursor()
        delete_query = "DELETE FROM radcheck WHERE id = %s"
        cur.execute(delete_query, (data_id,))
        mysql.connection.commit()
        cur.close()

 
        return redirect(url_for('client'))
    except Exception as e:
        return str(e)


@app.route('/deleteclient', methods=['POST'])
def delete_cliet():
    try:
        data_id = request.form.get('id')
        cur = mysql.connection.cursor()
        delete_query = "DELETE FROM userclient WHERE id = %s"
        cur.execute(delete_query, (data_id,))
        mysql.connection.commit()
        cur.close()

 
        return redirect(url_for('tambah'))
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
