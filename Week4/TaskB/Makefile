# ==============================================================================
# Makefile: Otomasi Eksekusi ZMQ Parallel Pipeline (Week 4 - Task B)
# ==============================================================================

PYTHON = python

.PHONY: all help dist worker-1 worker-2 collector run-workers run-pipeline stop clean

help:
	@echo ==============================================================================
	@echo Panduan Perintah Makefile Task B (Push-Pull Parallel Pipeline)
	@echo ==============================================================================
	@echo   make dist         - Menjalankan Tasks Distributor (Push port 9921)
	@echo   make worker-1     - Menjalankan Worker 1 (Pull 9921, Push port 9933)
	@echo   make worker-2     - Menjalankan Worker 2 (Pull 9921, Push port 9932)
	@echo   make collector    - Menjalankan Tasks Collector (Pull 9933 & 9932)
	@echo   make run-workers  - Menjalankan Worker 1 dan Worker 2 di background
	@echo   make run-pipeline - Menjalankan Collector dan kedua Worker di background, lalu Distributor
	@echo   make stop         - Menghentikan seluruh proses Worker, Collector, dan Distributor
	@echo   make clean        - Membersihkan berkas log sementara
	@echo ==============================================================================

dist:
	$(PYTHON) distributor.py

worker-1:
	$(PYTHON) worker.py 1

worker-2:
	$(PYTHON) worker.py 2

collector:
	$(PYTHON) collector.py

run-workers:
	@echo [Makefile] Menjalankan Worker 1 dan Worker 2 di latar belakang...
	@start /B $(PYTHON) worker.py 1 > worker_1.log 2>&1
	@start /B $(PYTHON) worker.py 2 > worker_2.log 2>&1
	@echo [Makefile] Kedua Worker telah aktif!

run-pipeline:
	@echo [Makefile] Menjalankan Collector di latar belakang...
	@start /B $(PYTHON) collector.py > collector.log 2>&1
	@echo [Makefile] Menjalankan Worker 1 dan Worker 2 di latar belakang...
	@start /B $(PYTHON) worker.py 1 > worker_1.log 2>&1
	@start /B $(PYTHON) worker.py 2 > worker_2.log 2>&1
	@timeout /t 2 /nobreak >nul 2>&1 || sleep 2
	@echo [Makefile] Memulai Tasks Distributor...
	$(PYTHON) distributor.py

stop:
	@echo [Makefile] Menghentikan seluruh proses python distributor, worker, dan collector...
	-taskkill /F /IM python.exe 2>nul || true
	@echo [Makefile] Seluruh proses dihentikan.

clean: stop
	-del /Q *.log 2>nul || true
