from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Question, Answer, AnswerComment
from .forms import QuestionForm, AnswerForm, AnswerCommentForm
from Product.models import Product
from Business.models import Business
from django.db.models import Count
from Notification.models import Notification
from Tag.models import Tag
from HowTo.models import HowTo, HowToStep
import datetime

@login_required
def ask_question(request):
    product_id = request.GET.get('product')
    business_id = request.GET.get('business')
    step_id = request.GET.get('step')
    
    product = None
    business = None
    howto_step = None
    
    if product_id:
        product = get_object_or_404(Product, id=product_id)
    elif business_id:
        business = get_object_or_404(Business, id=business_id)
    elif step_id:
        howto_step = get_object_or_404(HowToStep, id=step_id)
        
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.product = product
            question.business = business
            question.howto_step = howto_step
            question.save()
            
            # Handle tags
            tags_input = form.cleaned_data.get('tags_input', '')
            if tags_input:
                for tag_name in tags_input.split(','):
                    tag_name = tag_name.strip()
                    if tag_name:
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        tag.questions.add(question)
            
            messages.success(request, 'Question asked successfully!')
            return redirect('QA:detail', question_id=question.id)
    else:
        form = QuestionForm()
        
    context = {
        'form': form,
        'product': product,
        'business': business,
        'howto_step': howto_step,
    }
    return render(request, 'QA/ask_question.html', context)

def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    
    # Increment view count
    question.views_count += 1
    question.save(update_fields=['views_count'])
    
    # Get answers with like count to help sorting
    # Accepted first, then by likes, then by date recent
    answers = question.answers.annotate(num_likes=Count('likes')).order_by('-is_accepted', '-num_likes', '-created_at')
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            
            # Trigger notification
            Notification.create_new_answer_notification(answer)
            
            messages.success(request, 'Answer posted!')
            return redirect('QA:detail', question_id=question.id)
    else:
        form = AnswerForm()
        
    context = {
        'question': question,
        'answers': answers,
        'form': form,
        'comment_form': AnswerCommentForm(),
    }
    return render(request, 'QA/question_detail.html', context)

@login_required
def post_answer_comment(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    if request.method == 'POST':
        form = AnswerCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.answer = answer
            comment.save()
            
            if request.headers.get('HX-Request'):
               # Return the full list of comments for this answer
               return render(request, 'QA/partials/answer_comments.html', {'answer': answer})
               
            return redirect('QA:detail', question_id=answer.question.id)
    return redirect('QA:detail', question_id=answer.question.id)

@login_required
def accept_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    question = answer.question
    
    # Only OP can accept
    if request.user == question.author:
        # Unaccept all other answers for this question (single acceptance policy)
        question.answers.update(is_accepted=False)
        answer.is_accepted = True
        answer.save()
        messages.success(request, 'Answer marked as accepted!')
    
    return redirect('QA:detail', question_id=question.id)

@login_required
def toggle_like_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    
    if request.user in answer.likes.all():
        answer.likes.remove(request.user)
    else:
        answer.likes.add(request.user)
        
    # Refresh to get updated count
    answer = Answer.objects.annotate(num_likes=Count('likes')).get(id=answer_id)
        
    # Return partial
    return render(request, 'QA/partials/answer_like_button.html', {'answer': answer})


def AllQuestionsListView(request):
    step_id = request.GET.get('step')
    
    if step_id:
        # Filter questions for a specific step
        step = get_object_or_404(HowToStep, id=step_id)
        questions = Question.objects.filter(howto_step=step).order_by('-created_at')
        title = f"Questions for {step.title if step.title else f'Step {step.order}'}"
        
        # Only include the step-specific questions, not all HowTo guides
        knowledge_items = []
        for q in questions:
            q.item_type = 'question'
            q.sorting_date = q.created_at
            knowledge_items.append(q)
        
        how_tos = []  # Empty since we don't want to show guides in step-specific view
    else:
        # Show all questions and guides
        questions = Question.objects.all().order_by('-created_at')
        how_tos = HowTo.objects.filter(is_public=True).order_by('-created_at')
        title = "All Questions"
        
        # Combined knowledge items for the directory
        knowledge_items = []
        
        for q in questions:
            q.item_type = 'question'
            q.sorting_date = q.created_at
            knowledge_items.append(q)
            
        for h in how_tos:
            h.item_type = 'howto'
            h.sorting_date = h.created_at
            knowledge_items.append(h)
        
        # Sort by date descending
        knowledge_items.sort(key=lambda x: x.sorting_date, reverse=True)
    
    return render(request, 'QA/allQuestions.html', {
        'knowledge_items': knowledge_items,
        'questions_count': questions.count(),
        'how_to_count': len(how_tos) if isinstance(how_tos, list) else how_tos.count(),
        'title': title,
        'step': step_id and step
    })
