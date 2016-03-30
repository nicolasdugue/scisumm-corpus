class fmax:

	def __init__(self, matrix_csr, matrix_csc, clustering, labels_line=[], labels_col=[]):

		self.matrix_csr = matrix_csr

		self.matrix_csc = matrix_csc

		self.clustering=clustering

		self.labels_line=labels_line

		self.labels_col=labels_col

		self.sum_rows=matrix_csr.sum(axis=1)

		self.sum_cols=matrix_csc.sum(axis=0)

		

	def sum_row(i):
		return self.sum_rows[i]

	def sum_col(i):
		return self.sum_cols[i]
		
