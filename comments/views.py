from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from products.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ArticleCommentForm, ProductCommentForm
from django.contrib import messages
from utilties.messaging import get_message
from articles.models import Article


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request):
        if not request.user.has_comment_permission:
            return HttpResponseForbidden(status=403)
        post_data, instance = request.POST, request.POST['instance']
        if instance == 'article':
            article = get_object_or_404(Article, id=post_data['article_id'])
            form = ArticleCommentForm(post_data)
            if form.is_valid():
                form.save(commit=False).add_comment(article, request.user)
                success_url = article.get_absolute_url()
            else:
                return render(request, 'article_detail.html', {'article': article, 'form': form})
        elif instance == 'product':
            product = get_object_or_404(Product, id=post_data['product_id'])
            form = ProductCommentForm(post_data)
            if form.is_valid():
                form.save(commit=False).add_comment(product, request.user)
                success_url = product.get_absolute_url()
            else:
                return render(request, 'product_detail.html', {'product': product, 'form': form})
        else:
            return HttpResponseBadRequest(status=400)
        messages.add_message(request, messages.INFO, get_message('comments/comment_submitted'))
        return redirect(success_url)
