import streamlit as st
from dl_config import process_download
import os
import io
from PyPDF2 import PdfWriter, PdfReader, PdfFileMerger
from pdf2docx import Converter
from docx2pdf import convert

st.set_page_config(page_title='My Tools', page_icon= '🛠️', layout='wide')

# main menu
st.sidebar.title("Μενού Εργαλείων")
app_mode = st.sidebar.selectbox("Επίλεξε εργαλείο:", ["YouTube Downloader", "PDF Split & Merge","Μετατροπέας (PDF <-> Word)"])

st.sidebar.markdown("---") 

# ΕΡΓΑΛΕΙΟ 1: YOUTUBE DOWNLOADER
if app_mode == "YouTube Downloader":
    st.title('YouTube Video & Audio Downloader ')
    st.caption('Παρακαλώ εισάγετε url στο πεδίο αριστερά')

    video_url = st.sidebar.text_input('Enter:')

    col1, col2 = st.sidebar.columns(2)
    btn_mp4 = col1.button('Λήψη βίντεο (MP4)')
    btn_mp3 = col2.button('Λήψη ήχου (MP3)')

    if btn_mp4 or btn_mp3:
        if not video_url:
            st.warning("Πρέπει να εισάγετε url:")
        else:
            selected_format = 'mp4' if btn_mp4 else 'mp3'
            selected_mime = 'video/mp4' if btn_mp4 else 'audio/mpeg'

            download_file_path = process_download(video_url, format_type=selected_format)
            
            if download_file_path:
                try:
                    with open(download_file_path, 'rb') as f:
                        file_bytes = f.read()
                    
                    file_name = os.path.basename(download_file_path)

                    st.download_button(
                        label=f'Λήψη {selected_format.upper()}',
                        data=file_bytes,
                        file_name=file_name,
                        mime=selected_mime
                    )
                    st.success(f'Prepared {selected_format.upper()} Successfully!')
                    os.remove(download_file_path)
                except Exception as e:
                    st.error(f'Could not prepare the file: {e}')


# ΕΡΓΑΛΕΙΟ 2: PDF SPLIT & MERGE

elif app_mode == "PDF Split & Merge":
    st.title('PDF Splitter & Merger 📄')
    
    action = st.radio("Τι θέλεις να κάνεις;", ["Split", "Merge"])

    # --- ΛΕΙΤΟΥΡΓΙΑ SPLIT ---
    if action == "Split":
        st.caption("Ανέβασε ένα PDF και επίλεξε σε ποια σελίδα θα κοπεί.")
        uploaded_file = st.file_uploader("Επίλεξε αρχείο PDF:", type="pdf")
        
        if uploaded_file:
            reader = PdfReader(uploaded_file)
            total_pages = len(reader.pages)
            
            st.info(f"Το έγγραφό έχει συνολικά {total_pages} σελίδες.")
            
            if total_pages > 1:
                # σημειο κοπης
                split_page = st.number_input(
                    "Επίλεξε την σελίδα που θα κοπεί το αρχείο", 
                    min_value=1, max_value=total_pages-1, value=total_pages//2
                )
                
                if st.button("Διαχωρισμός"):

                    writer1 = PdfWriter()
                    writer2 = PdfWriter()
                    
                    # απο αρχη σε σελιδα
                    for i in range(split_page):
                        writer1.add_page(reader.pages[i])
                        
                    # απο σελιδα
                    for i in range(split_page, total_pages):
                        writer2.add_page(reader.pages[i])
                        
                    
                    output_pdf1 = io.BytesIO()
                    writer1.write(output_pdf1)
                    
                    output_pdf2 = io.BytesIO()
                    writer2.write(output_pdf2)
                    
                    st.success("Το αρχείο χωρίστηκε")
                    
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label=f"📥 Μέρος 1 (Σελ. 1-{split_page})",
                            data=output_pdf1.getvalue(),
                            file_name="part1.pdf",
                            mime="application/pdf"
                        )
                    with col2:
                        st.download_button(
                            label=f"📥 Μέρος 2 (Σελ. {split_page + 1}-{total_pages})",
                            data=output_pdf2.getvalue(),
                            file_name="part2.pdf",
                            mime="application/pdf"
                        )
            else:
                st.warning("Αυτό το PDF έχει μόνο 1 σελίδα")

    # --- ΛΕΙΤΟΥΡΓΙΑ MERGE ---
    elif action == "Merge":
        st.caption("Ανέβασε 2 ή περισσότερα αρχεία για να τα ενώσεις.")
        uploaded_files = st.file_uploader("Επίλεξε αρχεία PDF:", type="pdf", accept_multiple_files=True)
        
        if uploaded_files and len(uploaded_files) > 1 and st.button("Συγχώνευση"):
            merger = PdfWriter()
            
            for pdf in uploaded_files:
                merger.append(pdf)
                
            output_pdf = io.BytesIO()
            merger.write(output_pdf)
            
            st.success("Τα αρχεία ενώθηκαν")
            st.download_button(
                label="Κατέβασμα ενωμένου PDF",
                data=output_pdf.getvalue(),
                file_name="merged.pdf",
                mime="application/pdf"
            )
        elif uploaded_files and len(uploaded_files) < 2:
            st.warning("Παρακαλώ ανέβασε τουλάχιστον 2 αρχεία.")
    # ---------------------------------------------------------
# ΕΡΓΑΛΕΙΟ 3: CONVERTER (PDF <-> WORD)
# ---------------------------------------------------------
elif app_mode == "Μετατροπέας (PDF <-> Word)":
    st.title('Μετατροπέας Αρχείων 🔄')
    
    conversion_type = st.radio("Τι είδους μετατροπή θέλεις;", ["Από PDF σε Word", "Από Word σε PDF"])
    
    # --- PDF ΣΕ WORD ---
    if conversion_type == "Από PDF σε Word":
        st.caption("Ανέβασε αρχείο PDF για να το κάνεις επεξεργάσιμο έγγραφο Word (.docx).")
        uploaded_file = st.file_uploader("Επίλεξε αρχείο PDF:", type="pdf")
        
        if uploaded_file and st.button("Μετατροπή σε Word"):
            with st.spinner("Γίνεται μετατροπή σε Word, παρακαλώ περίμενε..."):
                # Οι βιβλιοθήκες αυτές χρειάζονται τα αρχεία στον δίσκο για να δουλέψουν
                with open("temp_in.pdf", "wb") as f:
                    f.write(uploaded_file.getvalue())
                    
                # Μετατροπή
                cv = Converter("temp_in.pdf")
                cv.convert("temp_out.docx")
                cv.close()
                
                # Διάβασμα νέου αρχείου για το κατέβασμα
                with open("temp_out.docx", "rb") as f:
                    docx_bytes = f.read()
                    
                # Καθάρισμα του δίσκου μας (όπως κάναμε στο YouTube)
                os.remove("temp_in.pdf")
                os.remove("temp_out.docx")
                
            st.success("Έτοιμο!")
            st.download_button(
                label="📥 Κατέβασμα Word", 
                data=docx_bytes, 
                file_name="converted_document.docx", 
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            
    # --- WORD ΣΕ PDF ---
    elif conversion_type == "Από Word σε PDF":
        st.caption("Ανέβασε αρχείο Word (.docx) για να το κάνεις PDF.")
        uploaded_file = st.file_uploader("Επίλεξε αρχείο Word:", type="docx")
        
        if uploaded_file and st.button("Μετατροπή σε PDF"):
            with st.spinner("Γίνεται μετατροπή σε PDF, παρακαλώ περίμενε..."):
                with open("temp_in.docx", "wb") as f:
                    f.write(uploaded_file.getvalue())
                    
                # Μετατροπή μέσω του docx2pdf
                convert("temp_in.docx", "temp_out.pdf")
                
                with open("temp_out.pdf", "rb") as f:
                    pdf_bytes = f.read()
                    
                os.remove("temp_in.docx")
                os.remove("temp_out.pdf")
                
            st.success("Έτοιμο!")
            st.download_button(
                label="📥 Κατέβασμα PDF", 
                data=pdf_bytes, 
                file_name="converted_document.pdf", 
                mime="application/pdf"
            )